SELECT
    strike
    , bid
    , ask
    , strike * 100 as capital_required
    , bid * 100 as total_premium
    , (total_premium / capital_required) * 100 as return
    , return * (365 / {DTE}) as annualized_return
FROM {tbl}
WHERE
    1=1
    AND inTheMoney is False
    AND bid > 0