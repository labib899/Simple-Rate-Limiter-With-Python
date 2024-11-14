local key = KEYS[1] 
local limit = tonumber(ARGV[1])
local refill_time = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])


local tokens = redis.call("get", key)
if not tokens then
    tokens = limit  
else
    tokens = tonumber(tokens)
end

local last_refill = redis.call("get", key .. ":last_refill")
if not last_refill then
    last_refill = current_time
else
    last_refill = tonumber(last_refill)
end


local refill_count = math.floor((current_time - last_refill) / refill_time)
tokens = math.min(limit, tokens + refill_count)

redis.call("set", key .. ":last_refill", current_time)

if tokens > 0 then
    redis.call("setex", key, refill_time, tokens - 1)  
    return tokens - 1 
else
    return -1 
end
