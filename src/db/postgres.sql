-- 1. Create the table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merchant_category VARCHAR(50)
);

-- 2. Insert Normal Data (User 101 usually spends small amounts)
INSERT INTO transactions (user_id, amount, merchant_category, transaction_date) VALUES 
(101, 45.50, 'Groceries', NOW() - INTERVAL '10 days'),
(101, 52.00, 'Dining', NOW() - INTERVAL '9 days'),
(101, 30.00, 'Transport', NOW() - INTERVAL '8 days'),
(101, 60.25, 'Groceries', NOW() - INTERVAL '7 days'),
(101, 48.75, 'Dining', NOW() - INTERVAL '6 days'),
(101, 55.00, 'Utilities', NOW() - INTERVAL '5 days');

-- 3. Insert the ANOMALY (The Fraud Case for User 101)
-- This value ($5,000) is statistically huge compared to the rows above.
INSERT INTO transactions (user_id, amount, merchant_category, transaction_date) VALUES 
(101, 5000.00, 'Electronics', NOW() - INTERVAL '1 hour');

-- 4. Insert data for another user (User 102 - Normal behavior)
INSERT INTO transactions (user_id, amount, merchant_category, transaction_date) VALUES 
(102, 120.00, 'Retail', NOW() - INTERVAL '3 days'),
(102, 110.00, 'Retail', NOW() - INTERVAL '2 days'),
(102, 130.00, 'Dining', NOW() - INTERVAL '1 day');