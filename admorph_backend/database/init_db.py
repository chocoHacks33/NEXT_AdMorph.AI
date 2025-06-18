#!/usr/bin/env python3
"""
Database initialization script for AdMorph.AI
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path
from typing import Optional

# Add the parent directory to the path so we can import from admorph_backend
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import get_settings


class DatabaseInitializer:
    """Initialize and setup the AdMorph.AI database"""
    
    def __init__(self):
        self.settings = get_settings()
        self.schema_file = Path(__file__).parent / "schema.sql"
    
    async def create_database_if_not_exists(self):
        """Create the database if it doesn't exist"""
        print("🔍 Checking if database exists...")
        
        # Connect to postgres database to create our database
        postgres_url = self.settings.database_url.replace(f"/{self.settings.postgres_db}", "/postgres")
        
        try:
            conn = await asyncpg.connect(postgres_url)
            
            # Check if database exists
            result = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1",
                self.settings.postgres_db
            )
            
            if not result:
                print(f"📦 Creating database '{self.settings.postgres_db}'...")
                await conn.execute(f'CREATE DATABASE "{self.settings.postgres_db}"')
                print("✅ Database created successfully")
            else:
                print("✅ Database already exists")
            
            await conn.close()
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            raise
    
    async def run_schema(self):
        """Run the database schema"""
        print("🏗️  Setting up database schema...")
        
        if not self.schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_file}")
        
        # Read schema file
        with open(self.schema_file, 'r') as f:
            schema_sql = f.read()
        
        try:
            conn = await asyncpg.connect(self.settings.database_url)
            
            # Execute schema
            await conn.execute(schema_sql)
            print("✅ Database schema applied successfully")
            
            await conn.close()
            
        except Exception as e:
            print(f"❌ Error applying schema: {e}")
            raise
    
    async def verify_setup(self):
        """Verify the database setup is correct"""
        print("🔍 Verifying database setup...")
        
        try:
            conn = await asyncpg.connect(self.settings.database_url)
            
            # Check if main tables exist
            tables_to_check = [
                'business_profiles',
                'demographic_segments', 
                'ad_variants',
                'base_products',
                'product_variants',
                'campaigns',
                'ab_tests'
            ]
            
            for table in tables_to_check:
                result = await conn.fetchval(
                    "SELECT to_regclass($1)",
                    f"public.{table}"
                )
                if result:
                    print(f"  ✅ Table '{table}' exists")
                else:
                    print(f"  ❌ Table '{table}' missing")
                    raise Exception(f"Table {table} not found")
            
            # Check sample data
            business_count = await conn.fetchval("SELECT COUNT(*) FROM business_profiles")
            print(f"  📊 Sample businesses: {business_count}")
            
            await conn.close()
            print("✅ Database verification completed successfully")
            
        except Exception as e:
            print(f"❌ Database verification failed: {e}")
            raise
    
    async def initialize(self, force_recreate: bool = False):
        """Initialize the complete database"""
        print("🤖 AdMorph.AI Database Initialization")
        print("=" * 50)
        
        try:
            # Create database if needed
            await self.create_database_if_not_exists()
            
            # Apply schema
            if force_recreate:
                print("⚠️  Force recreate mode - dropping existing schema...")
                conn = await asyncpg.connect(self.settings.database_url)
                await conn.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
                await conn.close()
            
            await self.run_schema()
            
            # Verify setup
            await self.verify_setup()
            
            print("\n🎉 Database initialization completed successfully!")
            print(f"📍 Database URL: {self.settings.database_url}")
            print(f"🏢 Sample business profiles created")
            print(f"📊 Ready for AdMorph.AI operations")
            
        except Exception as e:
            print(f"\n❌ Database initialization failed: {e}")
            sys.exit(1)


async def main():
    """Main initialization function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize AdMorph.AI database")
    parser.add_argument(
        "--force-recreate", 
        action="store_true",
        help="Force recreate the database schema (WARNING: This will delete all data)"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true", 
        help="Only verify the database setup without making changes"
    )
    
    args = parser.parse_args()
    
    initializer = DatabaseInitializer()
    
    if args.verify_only:
        print("🔍 Verification mode - checking database setup...")
        await initializer.verify_setup()
    else:
        await initializer.initialize(force_recreate=args.force_recreate)


if __name__ == "__main__":
    # Check environment
    if not os.getenv("DATABASE_URL") and not os.getenv("POSTGRES_HOST"):
        print("❌ Database configuration not found!")
        print("Please set DATABASE_URL or POSTGRES_* environment variables")
        print("\nExample:")
        print("export DATABASE_URL=postgresql://user:password@localhost:5432/admorph")
        print("or")
        print("export POSTGRES_HOST=localhost")
        print("export POSTGRES_USER=admorph") 
        print("export POSTGRES_PASSWORD=password")
        print("export POSTGRES_DB=admorph")
        sys.exit(1)
    
    # Run initialization
    asyncio.run(main())
