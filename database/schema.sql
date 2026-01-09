-- Kalai Medical Center - Database Schema
-- Run this in your Supabase SQL Editor

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    image_url TEXT,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access (only active products)
CREATE POLICY "Public products are viewable by everyone"
ON products FOR SELECT
USING (is_active = true);

-- Create policy for service role (full access)
CREATE POLICY "Service role has full access"
ON products FOR ALL
USING (auth.role() = 'service_role');

-- Insert some sample products (optional - for testing)
INSERT INTO products (name, description, price, stock, category, image_url) VALUES
('Limpieza Facial Profunda', 'Tratamiento completo de limpieza facial con extracción y mascarilla', 35000, 100, 'Faciales', NULL),
('Masaje Relajante', 'Masaje corporal completo de 60 minutos', 45000, 50, 'Masajes', NULL),
('Tratamiento Anti-Edad', 'Tratamiento facial rejuvenecedor con tecnología avanzada', 65000, 30, 'Faciales', NULL);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
