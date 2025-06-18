"""
Background job processing system for AdMorph.AI
Handles AI generation, personalization, and other long-running tasks
"""

import asyncio
import uuid
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import redis.asyncio as redis

from ..config.settings import get_settings
from ..api.websockets import (
    broadcast_generation_update,
    broadcast_personalization_update,
    broadcast_ab_test_update
)

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobType(Enum):
    AD_GENERATION = "ad_generation"
    PRODUCT_PERSONALIZATION = "product_personalization"
    AB_TEST_ANALYSIS = "ab_test_analysis"
    DEMOGRAPHIC_ANALYSIS = "demographic_analysis"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    VOICE_PROCESSING = "voice_processing"


class BackgroundJob:
    """Represents a background job"""
    
    def __init__(
        self,
        job_id: str,
        job_type: JobType,
        business_id: str,
        input_data: Dict[str, Any],
        priority: int = 5
    ):
        self.job_id = job_id
        self.job_type = job_type
        self.business_id = business_id
        self.input_data = input_data
        self.priority = priority
        self.status = JobStatus.PENDING
        self.progress = 0
        self.result_data = None
        self.error_message = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.retry_count = 0
        self.max_retries = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary"""
        return {
            "job_id": self.job_id,
            "job_type": self.job_type.value,
            "business_id": self.business_id,
            "input_data": self.input_data,
            "priority": self.priority,
            "status": self.status.value,
            "progress": self.progress,
            "result_data": self.result_data,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackgroundJob':
        """Create job from dictionary"""
        job = cls(
            job_id=data["job_id"],
            job_type=JobType(data["job_type"]),
            business_id=data["business_id"],
            input_data=data["input_data"],
            priority=data["priority"]
        )
        
        job.status = JobStatus(data["status"])
        job.progress = data["progress"]
        job.result_data = data["result_data"]
        job.error_message = data["error_message"]
        job.created_at = datetime.fromisoformat(data["created_at"])
        job.started_at = datetime.fromisoformat(data["started_at"]) if data["started_at"] else None
        job.completed_at = datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None
        job.retry_count = data["retry_count"]
        job.max_retries = data["max_retries"]
        
        return job


class JobManager:
    """Manages background jobs using Redis as queue"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client = None
        self.job_handlers: Dict[JobType, Callable] = {}
        self.active_jobs: Dict[str, BackgroundJob] = {}
        self.worker_running = False
    
    async def initialize(self):
        """Initialize job manager"""
        try:
            redis_url = getattr(self.settings, 'redis_url', 'redis://localhost:6379/0')
            self.redis_client = redis.from_url(redis_url)
            
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ Job manager initialized with Redis connection")
            
            # Register job handlers
            self._register_handlers()
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize job manager: {e}")
            raise
    
    def _register_handlers(self):
        """Register job type handlers"""
        from ..services.ai_service import openai_service
        from ..services.product_service import product_service
        
        self.job_handlers = {
            JobType.AD_GENERATION: self._handle_ad_generation,
            JobType.PRODUCT_PERSONALIZATION: self._handle_product_personalization,
            JobType.AB_TEST_ANALYSIS: self._handle_ab_test_analysis,
            JobType.DEMOGRAPHIC_ANALYSIS: self._handle_demographic_analysis,
            JobType.PERFORMANCE_OPTIMIZATION: self._handle_performance_optimization,
            JobType.VOICE_PROCESSING: self._handle_voice_processing
        }
    
    async def submit_job(
        self,
        job_type: JobType,
        business_id: str,
        input_data: Dict[str, Any],
        priority: int = 5
    ) -> str:
        """Submit a new background job"""
        
        job_id = str(uuid.uuid4())
        job = BackgroundJob(
            job_id=job_id,
            job_type=job_type,
            business_id=business_id,
            input_data=input_data,
            priority=priority
        )
        
        # Store job in Redis
        await self.redis_client.hset(
            f"job:{job_id}",
            mapping={"data": json.dumps(job.to_dict())}
        )
        
        # Add to priority queue
        await self.redis_client.zadd(
            "job_queue",
            {job_id: priority}
        )
        
        logger.info(f"Job {job_id} submitted: {job_type.value}")
        return job_id
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        job_data = await self.redis_client.hget(f"job:{job_id}", "data")
        if not job_data:
            return None
        
        job_dict = json.loads(job_data)
        return {
            "job_id": job_dict["job_id"],
            "status": job_dict["status"],
            "progress": job_dict["progress"],
            "result": job_dict["result_data"],
            "error": job_dict["error_message"],
            "created_at": job_dict["created_at"],
            "completed_at": job_dict["completed_at"]
        }
    
    async def start_worker(self):
        """Start background job worker"""
        if self.worker_running:
            return
        
        self.worker_running = True
        logger.info("🚀 Starting background job worker...")
        
        while self.worker_running:
            try:
                # Get next job from priority queue
                job_data = await self.redis_client.bzpopmin("job_queue", timeout=5)
                
                if job_data:
                    queue_name, job_id, priority = job_data
                    job_id = job_id.decode('utf-8')
                    
                    # Get job details
                    job_json = await self.redis_client.hget(f"job:{job_id}", "data")
                    if job_json:
                        job_dict = json.loads(job_json)
                        job = BackgroundJob.from_dict(job_dict)
                        
                        # Process job
                        await self._process_job(job)
                
            except Exception as e:
                logger.error(f"Error in job worker: {e}")
                await asyncio.sleep(1)
    
    async def stop_worker(self):
        """Stop background job worker"""
        self.worker_running = False
        logger.info("🛑 Background job worker stopped")
    
    async def _process_job(self, job: BackgroundJob):
        """Process a single job"""
        try:
            logger.info(f"Processing job {job.job_id}: {job.job_type.value}")
            
            # Update job status
            job.status = JobStatus.RUNNING
            job.started_at = datetime.now()
            await self._update_job(job)
            
            # Get handler
            handler = self.job_handlers.get(job.job_type)
            if not handler:
                raise ValueError(f"No handler for job type: {job.job_type.value}")
            
            # Execute handler
            result = await handler(job)
            
            # Update job with result
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.result_data = result
            job.completed_at = datetime.now()
            await self._update_job(job)
            
            logger.info(f"Job {job.job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Job {job.job_id} failed: {e}")
            
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.retry_count += 1
            job.completed_at = datetime.now()
            await self._update_job(job)
            
            # Retry if under limit
            if job.retry_count < job.max_retries:
                logger.info(f"Retrying job {job.job_id} (attempt {job.retry_count + 1})")
                await asyncio.sleep(60)  # Wait before retry
                await self.redis_client.zadd("job_queue", {job.job_id: job.priority})
    
    async def _update_job(self, job: BackgroundJob):
        """Update job in Redis"""
        await self.redis_client.hset(
            f"job:{job.job_id}",
            mapping={"data": json.dumps(job.to_dict())}
        )
        
        # Broadcast update via WebSocket
        if job.job_type == JobType.AD_GENERATION:
            await broadcast_generation_update(
                job.job_id, job.status.value, job.progress, job.result_data
            )
        elif job.job_type == JobType.PRODUCT_PERSONALIZATION:
            await broadcast_personalization_update(
                job.job_id, job.status.value, job.progress, job.result_data
            )
    
    # Job handlers
    async def _handle_ad_generation(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle ad generation job"""
        from ..services.ai_service import openai_service
        
        # Simulate ad generation process
        job.progress = 25
        await self._update_job(job)
        
        # Generate ad copy
        result = await openai_service.generate_ad_copy(
            job.input_data.get('business_profile', {}),
            job.input_data.get('demographic', {}),
            job.input_data.get('format_type', 'social')
        )
        
        job.progress = 75
        await self._update_job(job)
        
        # Additional processing...
        await asyncio.sleep(2)  # Simulate processing time
        
        return {
            "ad_variants": [result],
            "generation_strategy": "gpt4_ogilvy",
            "total_variants": 1
        }
    
    async def _handle_product_personalization(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle product personalization job"""
        from ..services.ai_service import openai_service
        
        job.progress = 20
        await self._update_job(job)
        
        # Personalize product
        result = await openai_service.personalize_product_copy(
            job.input_data.get('product', {}),
            job.input_data.get('demographic', {})
        )
        
        job.progress = 80
        await self._update_job(job)
        
        return {
            "personalized_variants": [result],
            "personalization_score": result.get('personalization_score', 0.8)
        }
    
    async def _handle_ab_test_analysis(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle A/B test analysis job"""
        # Simulate A/B test analysis
        await asyncio.sleep(3)
        
        return {
            "winner": "variant_a",
            "confidence": 0.95,
            "improvement": 15.2
        }
    
    async def _handle_demographic_analysis(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle demographic analysis job"""
        # Simulate demographic analysis
        await asyncio.sleep(2)
        
        return {
            "segments": ["tech_enthusiasts", "business_professionals"],
            "insights": ["High engagement with innovation messaging"]
        }
    
    async def _handle_performance_optimization(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle performance optimization job"""
        # Simulate performance optimization
        await asyncio.sleep(4)
        
        return {
            "optimizations": ["Increase bid on high-performing keywords"],
            "expected_improvement": 12.5
        }
    
    async def _handle_voice_processing(self, job: BackgroundJob) -> Dict[str, Any]:
        """Handle voice processing job"""
        from ..services.ai_service import voice_service
        
        # Process voice data
        audio_data = job.input_data.get('audio_data')
        if audio_data:
            # Convert base64 to bytes
            audio_bytes = base64.b64decode(audio_data)
            
            # Transcribe
            transcription = await voice_service.speech_to_text(audio_bytes)
            
            return {
                "transcription": transcription,
                "confidence": 0.95
            }
        
        return {"error": "No audio data provided"}


# Global job manager instance
job_manager = JobManager()
