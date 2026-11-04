
-- Add material_type column to Products table

ALTER TABLE Products
ADD COLUMN material_type TEXT;

-- Update material values

UPDATE Products
SET material_type = CASE product_id
    WHEN 101 THEN 'Bamboo'
    WHEN 102 THEN 'Cotton'
    WHEN 103 THEN 'Stainless Steel'
    WHEN 104 THEN 'Paper'
END;
