"""Change to BigInteger

Peek Plugin Database Migration Script

Revision ID: 0b20ccfb7a6a
Revises: 6c94c040e18c
Create Date: 2020-05-01 23:59:15.448423

"""

# revision identifiers, used by Alembic.
revision = '0b20ccfb7a6a'
down_revision = '6c94c040e18c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2

def _alterColumnPkBigInt(schemaName, tableName):
    return '''
        
        DO $$
            DECLARE
                rec RECORD;
            BEGIN
            FOR rec IN SELECT
                        tc.table_schema, 
                        tc.table_name, 
                        kcu.column_name
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                          AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                          AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_schema='%(schemaName)s'
                        AND ccu.table_name='%(tableName)s'
                        AND ccu.column_name='id'
            LOOP 
                EXECUTE 'ALTER TABLE "' || rec.table_schema || '"'
                        ||'."' || rec.table_name || '" '
                        || ' ALTER COLUMN "' || rec.column_name || '" TYPE bigint';
            END LOOP;
            END
        $$;
        
        ALTER TABLE %(schemaName)s."%(tableName)s" ALTER COLUMN id TYPE bigint;
        
        DROP SEQUENCE IF EXISTS %(schemaName)s."%(tableName)s_id_seq" CASCADE;

        CREATE SEQUENCE %(schemaName)s."%(tableName)s_id_seq" AS bigint
            INCREMENT 1
            START 1
            MINVALUE 0
            MAXVALUE 9223372036854775807
            CACHE 1000
            OWNED BY "%(schemaName)s"."%(tableName)s"."%(columnName)s";
    
        SELECT setval('%(schemaName)s."%(tableName)s_%(columnName)s_seq"', 
                max("%(columnName)s") + 1, FALSE)
        FROM %(schemaName)s."%(tableName)s";
        
        ALTER TABLE %(schemaName)s."%(tableName)s"
        ALTER COLUMN "%(columnName)s" SET DEFAULT 
            nextval('%(schemaName)s."%(tableName)s_%(columnName)s_seq"'::regclass);
        ''' % dict(schemaName=schemaName,
                   tableName=tableName,
                   columnName='id')


def upgrade():
    op.execute(_alterColumnPkBigInt("pl_docdb", "DocDbChunkQueue"))
    op.execute(_alterColumnPkBigInt("pl_docdb", "DocDbDocument"))
    op.execute(_alterColumnPkBigInt("pl_docdb", "DocDbEncodedChunkTuple"))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###