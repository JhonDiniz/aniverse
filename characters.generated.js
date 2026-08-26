// ARQUIVO GERADO AUTOMATICAMENTE por build_characters.py -- não edite na mão.
// Fonte: characters.py. Pra mudar personagens, edite lá e rode o script de novo.

const ANIMES = [
  "Dragon Ball",
  "One Piece",
  "Naruto"
];
const RAW = {
  "Dragon Ball": [
    [
      "Son Goku",
      "strong",
      "physical"
    ],
    [
      "Vegeta",
      "strong",
      "physical"
    ],
    [
      "Freeza",
      "strong",
      "magic"
    ],
    [
      "Broly",
      "strong",
      "physical"
    ],
    [
      "Bills",
      "strong",
      "hybrid"
    ],
    [
      "Vegito",
      "strong",
      "hybrid"
    ]
  ],
  "One Piece": [
    [
      "Monkey D. Luffy",
      "strong",
      "physical"
    ],
    [
      "Roronoa Zoro",
      "strong",
      "physical"
    ],
    [
      "Trafalgar Law",
      "strong",
      "magic"
    ],
    [
      "Tony Tony Chopper",
      "medium",
      "hybrid"
    ],
    [
      "Barba Branca",
      "strong",
      "physical"
    ],
    [
      "Barba Negra",
      "strong",
      "hybrid"
    ]
  ],
  "Naruto": [
    [
      "Naruto Shippuden B",
      "strong",
      "hybrid"
    ]
  ]
};
const CHAR_KIT = [
  {
    "vida": 234,
    "atk": 129,
    "defFis": 99,
    "defMag": 74,
    "vel": 114,
    "attacks": [
      {
        "name": "Soco Direto",
        "dmgType": "physical",
        "category": "melee",
        "power": 50,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Kamehameha",
        "dmgType": "physical",
        "category": "special",
        "power": 110,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 95,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Kaio-ken",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 25,
            "turns": 3
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 25,
            "turns": 3
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 231,
    "atk": 134,
    "defFis": 104,
    "defMag": 69,
    "vel": 112,
    "attacks": [
      {
        "name": "Soco do Orgulho Saiyajin",
        "dmgType": "physical",
        "category": "melee",
        "power": 52,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Big Bang Attack",
        "dmgType": "physical",
        "category": "special",
        "power": 115,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 93,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Investida Furiosa",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 28,
            "turns": 3
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 28,
            "turns": 3
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 208,
    "atk": 143,
    "defFis": 78,
    "defMag": 118,
    "vel": 103,
    "attacks": [
      {
        "name": "Golpe com a Cauda",
        "dmgType": "physical",
        "category": "melee",
        "power": 45,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Disco da Morte",
        "dmgType": "magic",
        "category": "special",
        "power": 115,
        "cooldown": 2,
        "effect": [
          {
            "kind": "dot",
            "target": "enemy",
            "flat": 15,
            "turns": 2
          }
        ],
        "effects": [
          {
            "kind": "dot",
            "target": "enemy",
            "flat": 15,
            "turns": 2
          }
        ],
        "onceOnly": false,
        "precision": 90,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Rajada de Energia Roxa",
        "dmgType": "magic",
        "category": "special",
        "power": 100,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 95,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 269,
    "atk": 144,
    "defFis": 109,
    "defMag": 49,
    "vel": 79,
    "attacks": [
      {
        "name": "Soco Bruto",
        "dmgType": "physical",
        "category": "melee",
        "power": 58,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Investida Selvagem",
        "dmgType": "physical",
        "category": "special",
        "power": 120,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 88,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Fúria Descontrolada",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 35,
            "turns": 3
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 35,
            "turns": 3
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 210,
    "atk": 130,
    "defFis": 90,
    "defMag": 100,
    "vel": 120,
    "attacks": [
      {
        "name": "Tapa Divino",
        "dmgType": "physical",
        "category": "melee",
        "power": 60,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 97,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Esfera de Destruição",
        "dmgType": "magic",
        "category": "special",
        "power": 125,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 90,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Fúria Comedida",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 239,
    "atk": 129,
    "defFis": 99,
    "defMag": 79,
    "vel": 104,
    "attacks": [
      {
        "name": "Soco Fusionado",
        "dmgType": "physical",
        "category": "melee",
        "power": 56,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Final Kamehameha",
        "dmgType": "physical",
        "category": "special",
        "power": 125,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 92,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Provocação Confiante",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "atk",
            "pct": -30
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "atk",
            "pct": -30
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 235,
    "atk": 140,
    "defFis": 105,
    "defMag": 60,
    "vel": 110,
    "attacks": [
      {
        "name": "Soco de Borracha",
        "dmgType": "physical",
        "category": "melee",
        "power": 52,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Gomu Gomu no Pistol",
        "dmgType": "physical",
        "category": "special",
        "power": 110,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 95,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Gear Second: Rajada",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "vel",
            "pct": 30,
            "turns": 3
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "vel",
            "pct": 30,
            "turns": 3
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 229,
    "atk": 149,
    "defFis": 114,
    "defMag": 54,
    "vel": 104,
    "attacks": [
      {
        "name": "Corte Rápido",
        "dmgType": "physical",
        "category": "melee",
        "power": 54,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Oni Giri",
        "dmgType": "physical",
        "category": "special",
        "power": 115,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 93,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Concentração: Ashura",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 30,
            "turns": 3
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "self",
            "stat": "atk",
            "pct": 30,
            "turns": 3
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 214,
    "atk": 139,
    "defFis": 84,
    "defMag": 114,
    "vel": 99,
    "attacks": [
      {
        "name": "Corte com Nodachi",
        "dmgType": "physical",
        "category": "melee",
        "power": 48,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "ROOM: Shambles",
        "dmgType": "magic",
        "category": "special",
        "power": 100,
        "cooldown": 2,
        "effect": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -30
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -30
          }
        ],
        "onceOnly": false,
        "precision": 92,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Counter Shock",
        "dmgType": "magic",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 45
          }
        ],
        "effects": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 45
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 211,
    "atk": 111,
    "defFis": 101,
    "defMag": 111,
    "vel": 116,
    "attacks": [
      {
        "name": "Chute de Rena",
        "dmgType": "physical",
        "category": "melee",
        "power": 35,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Rumble Ball: Guard Point",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "shield",
            "target": "self",
            "flat": 55
          }
        ],
        "effects": [
          {
            "kind": "shield",
            "target": "self",
            "flat": 55
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Kung-Fu Point: Investida",
        "dmgType": "physical",
        "category": "special",
        "power": 70,
        "cooldown": 2,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 272,
    "atk": 142,
    "defFis": 112,
    "defMag": 72,
    "vel": 52,
    "attacks": [
      {
        "name": "Soco Pesado",
        "dmgType": "physical",
        "category": "melee",
        "power": 58,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Gura Gura no Mi: Onda de Choque",
        "dmgType": "physical",
        "category": "special",
        "power": 125,
        "cooldown": 2,
        "effect": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "onceOnly": false,
        "precision": 88,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Presença Intimidadora",
        "dmgType": "physical",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 25
          }
        ],
        "effects": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 25
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 247,
    "atk": 127,
    "defFis": 97,
    "defMag": 102,
    "vel": 77,
    "attacks": [
      {
        "name": "Soco das Trevas",
        "dmgType": "physical",
        "category": "melee",
        "power": 50,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Yami Yami no Mi: Black Hole",
        "dmgType": "magic",
        "category": "special",
        "power": 110,
        "cooldown": 2,
        "effect": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "effects": [
          {
            "kind": "stat",
            "target": "enemy",
            "stat": "def",
            "pct": -35
          }
        ],
        "onceOnly": false,
        "precision": 90,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Onda de Choque Sombria",
        "dmgType": "magic",
        "category": "special",
        "power": 0,
        "cooldown": 3,
        "effect": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 35
          }
        ],
        "effects": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 35
          }
        ],
        "onceOnly": false,
        "precision": 100,
        "cost": 0,
        "targetType": "single"
      }
    ]
  },
  {
    "vida": 150,
    "atk": 125,
    "defFis": 95,
    "defMag": 90,
    "vel": 90,
    "attacks": [
      {
        "name": "Clone das Sombras",
        "dmgType": "physical",
        "category": "melee",
        "power": 40,
        "cooldown": 0,
        "effect": [
          {
            "kind": "nextDodge",
            "target": "self",
            "pct": 10
          }
        ],
        "effects": [
          {
            "kind": "nextDodge",
            "target": "self",
            "pct": 10
          }
        ],
        "onceOnly": false,
        "precision": 95,
        "cost": 0,
        "targetType": "single"
      },
      {
        "name": "Rasengan",
        "dmgType": "magic",
        "category": "melee",
        "power": 60,
        "cooldown": 0,
        "effect": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 20
          }
        ],
        "effects": [
          {
            "kind": "stun",
            "target": "enemy",
            "turns": 1,
            "chance": 20
          }
        ],
        "onceOnly": false,
        "precision": 85,
        "cost": 2,
        "targetType": "single"
      },
      {
        "name": "Rasen-Shuriken",
        "dmgType": "magic",
        "category": "melee",
        "power": 70,
        "cooldown": 0,
        "effect": null,
        "effects": [],
        "onceOnly": false,
        "precision": 75,
        "cost": 3,
        "targetType": "single",
        "ignoreFrontline": true
      }
    ]
  }
];
const APPEARANCE = [
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null
];
const CLASS_TYPE = [
  [
    "Guerreiro",
    "Normal"
  ],
  [
    "Guerreiro",
    "Normal"
  ],
  [
    "Mago",
    "Sombrio"
  ],
  [
    "Tanque",
    "Normal"
  ],
  [
    "Estrategista",
    "Sagrado"
  ],
  [
    "Guerreiro",
    "Sagrado"
  ],
  [
    "Lutador",
    "Normal"
  ],
  [
    "Espadachim",
    "Normal"
  ],
  [
    "Mago",
    "Espiritual"
  ],
  [
    "Suporte",
    "Natureza"
  ],
  [
    "Tanque",
    "Terra"
  ],
  [
    "Mago",
    "Sombrio"
  ],
  [
    "Guerreiro",
    "Vento"
  ]
];
const FOURTH_ATTACK = [
  {
    "name": "Genki Dama",
    "dmgType": "physical",
    "category": "special",
    "power": 135,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 80,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Final Flash",
    "dmgType": "physical",
    "category": "special",
    "power": 140,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 82,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Explosão Supernova",
    "dmgType": "magic",
    "category": "special",
    "power": 130,
    "cooldown": 4,
    "effect": [
      {
        "kind": "stat",
        "target": "enemy",
        "stat": "def",
        "pct": -30
      }
    ],
    "effects": [
      {
        "kind": "stat",
        "target": "enemy",
        "stat": "def",
        "pct": -30
      }
    ],
    "onceOnly": false,
    "precision": 80,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Explosão de Energia Bruta",
    "dmgType": "physical",
    "category": "special",
    "power": 145,
    "cooldown": 4,
    "effect": [
      {
        "kind": "stun",
        "target": "enemy",
        "turns": 1,
        "chance": 30
      }
    ],
    "effects": [
      {
        "kind": "stun",
        "target": "enemy",
        "turns": 1,
        "chance": 30
      }
    ],
    "onceOnly": false,
    "precision": 78,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Julgamento do Destruidor",
    "dmgType": "magic",
    "category": "special",
    "power": 140,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 85,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Big Bang Kamehameha",
    "dmgType": "magic",
    "category": "special",
    "power": 145,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 83,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Gomu Gomu no Elephant Gun",
    "dmgType": "physical",
    "category": "special",
    "power": 135,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 85,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Santoryu: Rashomon",
    "dmgType": "physical",
    "category": "special",
    "power": 140,
    "cooldown": 4,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 82,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Gamma Knife",
    "dmgType": "magic",
    "category": "special",
    "power": 125,
    "cooldown": 4,
    "effect": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 18,
        "turns": 2
      }
    ],
    "effects": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 18,
        "turns": 2
      }
    ],
    "onceOnly": false,
    "precision": 85,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Cura de Emergência",
    "dmgType": "magic",
    "category": "special",
    "power": 0,
    "cooldown": 3,
    "effect": [
      {
        "kind": "heal",
        "target": "self",
        "flat": 60
      }
    ],
    "effects": [
      {
        "kind": "heal",
        "target": "self",
        "flat": 60
      }
    ],
    "onceOnly": false,
    "precision": 100,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Terremoto Absoluto",
    "dmgType": "physical",
    "category": "special",
    "power": 150,
    "cooldown": 5,
    "effect": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 20,
        "turns": 2
      }
    ],
    "effects": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 20,
        "turns": 2
      }
    ],
    "onceOnly": false,
    "precision": 75,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Trevas Absolutas",
    "dmgType": "magic",
    "category": "special",
    "power": 135,
    "cooldown": 4,
    "effect": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 18,
        "turns": 2
      }
    ],
    "effects": [
      {
        "kind": "dot",
        "target": "enemy",
        "flat": 18,
        "turns": 2
      }
    ],
    "onceOnly": false,
    "precision": 82,
    "cost": 0,
    "targetType": "single"
  },
  {
    "name": "Transformação — Manto 4 Caudas",
    "dmgType": "physical",
    "category": "melee",
    "power": 0,
    "cooldown": 0,
    "effect": null,
    "effects": [],
    "onceOnly": false,
    "precision": 100,
    "cost": 5,
    "targetType": "single",
    "transformsInto": "manto_4_caudas"
  }
];
const RANK_OVERRIDE = {
  "Son Goku": "S",
  "Vegeta": "S",
  "Freeza": "S",
  "Broly": "S",
  "Bills": "S",
  "Vegito": "S",
  "Monkey D. Luffy": "S",
  "Roronoa Zoro": "S",
  "Trafalgar Law": "S",
  "Tony Tony Chopper": "S",
  "Barba Branca": "S",
  "Barba Negra": "S",
  "Naruto Shippuden B": "B"
};
const CHAR_FORMS = {
  "Naruto Shippuden B": {
    "manto_4_caudas": {
      "key": "manto_4_caudas",
      "name": "Manto 4 Caudas A",
      "vida": 170,
      "atk": 150,
      "defFis": 90,
      "defMag": 90,
      "vel": 100,
      "attacks": [
        {
          "name": "Força Bruta",
          "dmgType": "physical",
          "category": "melee",
          "power": 45,
          "cooldown": 0,
          "effect": null,
          "effects": [],
          "onceOnly": false,
          "precision": 95,
          "cost": 0,
          "targetType": "single"
        },
        {
          "name": "Manto Protetor",
          "dmgType": "physical",
          "category": "melee",
          "power": 0,
          "cooldown": 0,
          "effect": [
            {
              "kind": "healPctAtk",
              "target": "self",
              "pct": 30
            }
          ],
          "effects": [
            {
              "kind": "healPctAtk",
              "target": "self",
              "pct": 30
            }
          ],
          "onceOnly": false,
          "precision": 100,
          "cost": 2,
          "targetType": "single"
        },
        {
          "name": "Onda de Choque",
          "dmgType": "magic",
          "category": "melee",
          "power": 70,
          "cooldown": 0,
          "effect": null,
          "effects": [],
          "onceOnly": false,
          "precision": 70,
          "cost": 3,
          "targetType": "nearest_line_all"
        },
        {
          "name": "Mini Bijuudama",
          "dmgType": "magic",
          "category": "melee",
          "power": 110,
          "cooldown": 0,
          "effect": null,
          "effects": [],
          "onceOnly": false,
          "precision": 60,
          "cost": 5,
          "targetType": "mixed",
          "frontlineCount": 2,
          "backlineCount": 1
        }
      ]
    }
  }
};
const ART = {
  "Naruto Shippuden B": {
    "slug": "naruto",
    "states": [
      "base",
      "dash",
      "block"
    ],
    "facing": "left"
  }
};
