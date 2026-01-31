ATTR_TYPE = {
    # DB
    "balcony": "db",
    "elevator": "db",
    "furnished": "db",
    "pets": "db",
    "kreuzberg": "db",
    "neukoelln": "db",
    "charlottenburg": "db",
    "prenzlauerberg": "db",

    # weights (treat as db-like boolean vars in this prototype)
    "theta_price": "db",
    "theta_dist": "db",
    "theta_text": "db",

    # proximity/ordinal
    "price": "prox",
    "dist": "prox",
    "size": "prox",

    # text
    "quiet": "text",
    "modern": "text",
    "sunny": "text",
    "family": "text",
}

APARTMENTS = [
    {
        "name": "Apt1-Kreuzberg-Modern",
        "scores": {
            "kreuzberg": 1, "neukoelln": 0, "charlottenburg": 0, "prenzlauerberg": 0,
            "balcony": 1, "elevator": 0, "furnished": 1, "pets": 0,
            "price__low": 0.6, "price__mid": 0.8, "price__high": 0.2,
            "dist__near": 0.7, "dist__mid": 0.6, "dist__far": 0.2,
            "size__small": 0.3, "size__ok": 0.7, "size__large": 0.4,
            "quiet": 0.4, "modern": 0.9, "sunny": 0.6, "family": 0.3,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
    {
        "name": "Apt2-Neukoelln-Budget",
        "scores": {
            "kreuzberg": 0, "neukoelln": 1, "charlottenburg": 0, "prenzlauerberg": 0,
            "balcony": 0, "elevator": 0, "furnished": 0, "pets": 1,
            "price__low": 0.9, "price__mid": 0.5, "price__high": 0.1,
            "dist__near": 0.4, "dist__mid": 0.7, "dist__far": 0.3,
            "size__small": 0.6, "size__ok": 0.5, "size__large": 0.2,
            "quiet": 0.3, "modern": 0.4, "sunny": 0.5, "family": 0.4,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
    {
        "name": "Apt3-Charlottenburg-Quiet",
        "scores": {
            "kreuzberg": 0, "neukoelln": 0, "charlottenburg": 1, "prenzlauerberg": 0,
            "balcony": 1, "elevator": 1, "furnished": 0, "pets": 1,
            "price__low": 0.2, "price__mid": 0.6, "price__high": 0.8,
            "dist__near": 0.6, "dist__mid": 0.7, "dist__far": 0.2,
            "size__small": 0.2, "size__ok": 0.6, "size__large": 0.8,
            "quiet": 0.9, "modern": 0.5, "sunny": 0.5, "family": 0.7,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
    {
        "name": "Apt4-PrenzlauerBerg-Family",
        "scores": {
            "kreuzberg": 0, "neukoelln": 0, "charlottenburg": 0, "prenzlauerberg": 1,
            "balcony": 1, "elevator": 1, "furnished": 1, "pets": 1,
            "price__low": 0.3, "price__mid": 0.7, "price__high": 0.6,
            "dist__near": 0.8, "dist__mid": 0.5, "dist__far": 0.1,
            "size__small": 0.1, "size__ok": 0.6, "size__large": 0.9,
            "quiet": 0.7, "modern": 0.7, "sunny": 0.6, "family": 0.9,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
    {
        "name": "Apt5-Kreuzberg-Cheap-Far",
        "scores": {
            "kreuzberg": 1, "neukoelln": 0, "charlottenburg": 0, "prenzlauerberg": 0,
            "balcony": 0, "elevator": 0, "furnished": 0, "pets": 1,
            "price__low": 1.0, "price__mid": 0.4, "price__high": 0.0,
            "dist__near": 0.2, "dist__mid": 0.5, "dist__far": 0.7,
            "size__small": 0.7, "size__ok": 0.4, "size__large": 0.1,
            "quiet": 0.4, "modern": 0.3, "sunny": 0.4, "family": 0.2,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
    {
        "name": "Apt6-Charlottenburg-Lux",
        "scores": {
            "kreuzberg": 0, "neukoelln": 0, "charlottenburg": 1, "prenzlauerberg": 0,
            "balcony": 1, "elevator": 1, "furnished": 1, "pets": 0,
            "price__low": 0.0, "price__mid": 0.3, "price__high": 1.0,
            "dist__near": 0.7, "dist__mid": 0.6, "dist__far": 0.1,
            "size__small": 0.0, "size__ok": 0.4, "size__large": 1.0,
            "quiet": 0.8, "modern": 0.9, "sunny": 0.7, "family": 0.6,
            "theta_price": 0.8, "theta_dist": 0.7, "theta_text": 0.6,
        }
    },
]
