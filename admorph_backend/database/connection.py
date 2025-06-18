"""
Database connection and session management for AdMorph.AI
"""

import asyncio
import asyncpg
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import json

from ..config.settings import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations for AdMorph.AI"""
    
    def __init__(self):
        self.settings = get_settings()
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            logger.info("Initializing database connection pool...")
            self.pool = await asyncpg.create_pool(
                self.settings.database_url,
                min_size=5,
                max_size=20,
                command_timeout=60,
                server_settings={
                    'jit': 'off'  # Disable JIT for better performance with short queries
                }
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get a database connection from the pool"""
        if not self.pool:
            await self.initialize()
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts"""
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def execute_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Execute a SELECT query and return first result as dict"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def execute_scalar(self, query: str, *args) -> Any:
        """Execute a query and return a single value"""
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)
    
    async def execute_command(self, query: str, *args) -> str:
        """Execute an INSERT/UPDATE/DELETE command"""
        async with self.get_connection() as conn:
            return await conn.execute(query, *args)
    
    async def execute_transaction(self, queries: List[tuple]) -> List[Any]:
        """Execute multiple queries in a transaction"""
        async with self.get_connection() as conn:
            async with conn.transaction():
                results = []
                for query, args in queries:
                    result = await conn.execute(query, *args)
                    results.append(result)
                return results


# Global database manager instance
db_manager = DatabaseManager()


class BusinessProfileRepository:
    """Repository for business profile operations"""
    
    async def create(self, profile_data: Dict[str, Any]) -> str:
        """Create a new business profile"""
        query = """
        INSERT INTO business_profiles (
            business_name, industry, description, target_audience, 
            monthly_budget, campaign_goals, brand_voice, unique_selling_points,
            competitors, geographic_focus
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING business_id
        """
        
        result = await db_manager.execute_scalar(
            query,
            profile_data['business_name'],
            profile_data['industry'],
            profile_data['description'],
            json.dumps(profile_data.get('target_audience', {})),
            profile_data.get('monthly_budget', 0),
            profile_data.get('campaign_goals', []),
            profile_data.get('brand_voice', ''),
            profile_data.get('unique_selling_points', []),
            profile_data.get('competitors', []),
            profile_data.get('geographic_focus', [])
        )
        return str(result)
    
    async def get_by_id(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business profile by ID"""
        query = "SELECT * FROM business_profiles WHERE business_id = $1"
        result = await db_manager.execute_one(query, business_id)
        
        if result and result.get('target_audience'):
            # Parse JSON fields
            result['target_audience'] = json.loads(result['target_audience'])
        
        return result
    
    async def get_all(self) -> List[Dict[str, Any]]:
        """Get all business profiles"""
        query = "SELECT * FROM business_profiles ORDER BY created_at DESC"
        results = await db_manager.execute_query(query)
        
        # Parse JSON fields
        for result in results:
            if result.get('target_audience'):
                result['target_audience'] = json.loads(result['target_audience'])
        
        return results
    
    async def update(self, business_id: str, update_data: Dict[str, Any]) -> bool:
        """Update business profile"""
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in update_data.items():
            if key == 'target_audience':
                value = json.dumps(value)
            set_clauses.append(f"{key} = ${param_count}")
            values.append(value)
            param_count += 1
        
        if not set_clauses:
            return False
        
        query = f"""
        UPDATE business_profiles 
        SET {', '.join(set_clauses)}, updated_at = NOW()
        WHERE business_id = ${param_count}
        """
        values.append(business_id)
        
        result = await db_manager.execute_command(query, *values)
        return "UPDATE 1" in result


class AdVariantRepository:
    """Repository for ad variant operations"""
    
    async def create(self, variant_data: Dict[str, Any]) -> str:
        """Create a new ad variant"""
        query = """
        INSERT INTO ad_variants (
            business_id, demographic_segment_id, headline, body, cta,
            image_url, aesthetic_score, ogilvy_score, emotional_impact,
            format_type, generation_strategy, performance_score,
            trend_alignment, swipe_status
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        RETURNING variant_id
        """
        
        result = await db_manager.execute_scalar(
            query,
            variant_data['business_id'],
            variant_data.get('demographic_segment_id'),
            variant_data['headline'],
            variant_data['body'],
            variant_data['cta'],
            variant_data.get('image_url', ''),
            variant_data.get('aesthetic_score', 0.0),
            variant_data.get('ogilvy_score', 0.0),
            variant_data.get('emotional_impact', 0.0),
            variant_data.get('format_type', 'social'),
            variant_data.get('generation_strategy', 'default'),
            variant_data.get('performance_score', 0.0),
            variant_data.get('trend_alignment', 0.0),
            variant_data.get('swipe_status', 'pending')
        )
        return str(result)
    
    async def get_by_business(self, business_id: str) -> List[Dict[str, Any]]:
        """Get all ad variants for a business"""
        query = """
        SELECT av.*, ds.name as demographic_name
        FROM ad_variants av
        LEFT JOIN demographic_segments ds ON av.demographic_segment_id = ds.segment_id
        WHERE av.business_id = $1
        ORDER BY av.created_at DESC
        """
        return await db_manager.execute_query(query, business_id)
    
    async def update_performance(self, variant_id: str, performance_score: float) -> bool:
        """Update variant performance score"""
        query = """
        UPDATE ad_variants 
        SET performance_score = $1, updated_at = NOW()
        WHERE variant_id = $2
        """
        result = await db_manager.execute_command(query, performance_score, variant_id)
        return "UPDATE 1" in result


class ProductRepository:
    """Repository for product and e-commerce operations"""
    
    async def create_product(self, product_data: Dict[str, Any]) -> str:
        """Create a new base product"""
        query = """
        INSERT INTO base_products (
            product_id, business_id, name, description, price,
            category, features, images, platform, platform_product_id, metadata
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING product_id
        """
        
        await db_manager.execute_command(
            query,
            product_data['product_id'],
            product_data['business_id'],
            product_data['name'],
            product_data.get('description', ''),
            product_data.get('price', 0.0),
            product_data.get('category', ''),
            product_data.get('features', []),
            product_data.get('images', []),
            product_data.get('platform', 'shopify'),
            product_data.get('platform_product_id', ''),
            json.dumps(product_data.get('metadata', {}))
        )
        return product_data['product_id']
    
    async def create_variant(self, variant_data: Dict[str, Any]) -> str:
        """Create a personalized product variant"""
        query = """
        INSERT INTO product_variants (
            product_id, demographic_segment_id, personalized_title,
            personalized_description, highlighted_features, personalized_cta,
            price_positioning, urgency_messaging, social_proof,
            personalization_score, conversion_lift_estimate
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING variant_id
        """
        
        result = await db_manager.execute_scalar(
            query,
            variant_data['product_id'],
            variant_data.get('demographic_segment_id'),
            variant_data['personalized_title'],
            variant_data['personalized_description'],
            variant_data.get('highlighted_features', []),
            variant_data.get('personalized_cta', ''),
            variant_data.get('price_positioning', ''),
            variant_data.get('urgency_messaging', ''),
            variant_data.get('social_proof', []),
            variant_data.get('personalization_score', 0.0),
            variant_data.get('conversion_lift_estimate', 0.0)
        )
        return str(result)
    
    async def get_product_variants(self, product_id: str) -> List[Dict[str, Any]]:
        """Get all variants for a product"""
        query = """
        SELECT pv.*, ds.name as demographic_name
        FROM product_variants pv
        LEFT JOIN demographic_segments ds ON pv.demographic_segment_id = ds.segment_id
        WHERE pv.product_id = $1
        ORDER BY pv.personalization_score DESC
        """
        return await db_manager.execute_query(query, product_id)


# Repository instances
business_repo = BusinessProfileRepository()
ad_repo = AdVariantRepository()
product_repo = ProductRepository()


async def initialize_database():
    """Initialize database connection and repositories"""
    await db_manager.initialize()
    logger.info("Database repositories initialized")


async def close_database():
    """Close database connections"""
    await db_manager.close()
    logger.info("Database connections closed")
