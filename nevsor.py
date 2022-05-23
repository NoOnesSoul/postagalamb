nevek = [
    "Bádi Kristóf", "Basternák Zalán", "Boza Boglárka",
    "Emmer Bálint", "Fodor Martin", "Fónai Bálint",
    "Halama Samuel", "Herháger Gábor", "Janoschek Kristóf",
    "Juhász Máté", "Juhos Salamon", "Kocza Dániel",
    "Koós Máté", "Kozák György", "Lakatos Csaba",
    "Láng Kristóf", "Mayer Máté", "Paska Simon",
    "Petrovics Bence", "Rapati Tamás", "Récsei Botond",
    "Sinkó Rebeka", "Szakály Máté", "Szarka Kristóf",
    "Szivek István", "Tóthmajor Dóra", "Urbán Roland",
    "Valek Dániel", "Vollár Martin"
]

x = 39
a = x-1

def hetesek(het, nevsor):
    while het > 28:
        het -= 28
    b = het * 2
    c = b + 1
    while b > 28:
        b -= 28
        c -= 28
    if c > 28:
        c -= 28
    return f"**{nevsor[b]}** és **{nevsor[c]}** a hetesek."