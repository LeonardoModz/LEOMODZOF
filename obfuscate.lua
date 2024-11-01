local function decode(s)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s = string.gsub(s, "[^" .. b .. "=]", '')
    return (s:gsub('.', function(x)
        if x == '=' then return '' end
        local r, f = '', (b:find(x) - 1)
        for i = 6, 1, -1 do r = r .. (f % 2 ^ i - f % 2 ^ (i - 1) > 0 and '1' or '0') end
        return r;
    end):gsub('%d%d%d?%d?%d?%d?%d?', function(x)
        if (#x ~= 8) then return '' end
        local c = 0
        for i = 1, 8 do c = c + (x:sub(i, i) == '1' and 2 ^ (8 - i) or 0) end
        return string.char(c)
    end))
end

-- Nome da função e strings importantes em Base64 para evitar fácil leitura
local a = decode("c2V0VmVoaWNsZVBvc2l0aW9u")  -- "setVehiclePosition"
local b = function(c, d, e, f) a(c, d, e, f) end

-- Função principal para teleporte obfuscada
local c = function()
    b(1, 100, 200, 300)
end

-- Chamada da função
c()
