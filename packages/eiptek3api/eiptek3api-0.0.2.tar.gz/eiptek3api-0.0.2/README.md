# EIP Stats

url: <https://eip-tek3.epitest.eu>

pypi: <https://pypi.org/project/eiptek3api/>

## Usage

1. Login to eip website.
2. Open the console and write: `console.log(localStorage["token"])`
3. Write the token in a file named `.bearer`
4. Run `make stats` in a terminal

## Doc

```bash
# stats for all projects with no filters
make stats
# stats for projects with tags containing 'Machine Learning'
make stats FILTERS='"tags__label__eq=Machine Learning"'
# stats for projects in Paris and tags containing 'Machine Learning'
make stats FILTERS='"tags__label__eq=Machine Learning" "owner_city__name__eq=Paris"'
# stats for projects containing 'eco' in the description
make stats FILTERS='"description__contains=eco"'
```

---

### 11:51 - 2024-06-24

<details>
<summary>Click for stats</summary>

```json
{
"number_of_projects": 193 
,
"number_of_projects_by_cities": {
    "Paris": 37,
    "Lyon": 22,
    "Cotonou": 19,
    "Toulouse": 14,
    "Montpellier": 13,
    "Strasbourg": 12,
    "Nice": 10,
    "Marseille": 10,
    "Rennes": 10,
    "Bordeaux": 9,
    "Lille": 8,
    "Nancy": 8,
    "Nantes": 7,
    "La R\u00e9union": 6,
    "Barcelona": 4,
    "Mulhouse": 2,
    "Berlin": 1,
    "Bruxelles": 1
} 
,
"status_all_cities": {
    "waiting_update": 73,
    "rejected": 64,
    "approved": 29,
    "draft": 27
} 
,
"status_by_cities": {
    "Cotonou": {
        "draft": 17,
        "waiting_update": 1,
        "rejected": 1
    },
    "La R\u00e9union": {
        "waiting_update": 6
    },
    "Lille": {
        "rejected": 3,
        "waiting_update": 3,
        "approved": 2
    },
    "Nantes": {
        "approved": 3,
        "rejected": 2,
        "draft": 1,
        "waiting_update": 1
    },
    "Lyon": {
        "waiting_update": 11,
        "rejected": 7,
        "approved": 3,
        "draft": 1
    },
    "Paris": {
        "rejected": 15,
        "waiting_update": 11,
        "approved": 7,
        "draft": 4
    },
    "Toulouse": {
        "waiting_update": 7,
        "rejected": 6,
        "draft": 1
    },
    "Nice": {
        "waiting_update": 4,
        "rejected": 3,
        "approved": 2,
        "draft": 1
    },
    "Nancy": {
        "rejected": 4,
        "waiting_update": 3,
        "approved": 1
    },
    "Strasbourg": {
        "rejected": 7,
        "waiting_update": 2,
        "approved": 2,
        "draft": 1
    },
    "Marseille": {
        "rejected": 5,
        "waiting_update": 4,
        "approved": 1
    },
    "Montpellier": {
        "rejected": 6,
        "waiting_update": 5,
        "approved": 1,
        "draft": 1
    },
    "Bordeaux": {
        "rejected": 4,
        "waiting_update": 4,
        "approved": 1
    },
    "Rennes": {
        "waiting_update": 6,
        "approved": 3,
        "rejected": 1
    },
    "Barcelona": {
        "approved": 3,
        "waiting_update": 1
    },
    "Mulhouse": {
        "waiting_update": 2
    },
    "Berlin": {
        "waiting_update": 1
    },
    "Bruxelles": {
        "waiting_update": 1
    }
}
}
```

</details>

### 13:45 - 2024-06-24

<details>
<summary>Click for stats</summary>

```json
{
"number_of_projects": 194 
,
"number_of_projects_by_cities": {
    "Paris": 37,
    "Lyon": 22,
    "Cotonou": 19,
    "Toulouse": 14,
    "Strasbourg": 13,
    "Montpellier": 13,
    "Nice": 10,
    "Marseille": 10,
    "Rennes": 10,
    "Bordeaux": 9,
    "Lille": 8,
    "Nancy": 8,
    "Nantes": 7,
    "La R\u00e9union": 6,
    "Barcelona": 4,
    "Mulhouse": 2,
    "Berlin": 1,
    "Bruxelles": 1
} 
,
"status_all_cities": {
    "waiting_update": 73,
    "rejected": 64,
    "approved": 29,
    "draft": 28
} 
,
"status_by_cities": {
    "Strasbourg": {
        "rejected": 7,
        "draft": 2,
        "waiting_update": 2,
        "approved": 2
    },
    "Cotonou": {
        "draft": 17,
        "waiting_update": 1,
        "rejected": 1
    },
    "La R\u00e9union": {
        "waiting_update": 6
    },
    "Lille": {
        "rejected": 3,
        "waiting_update": 3,
        "approved": 2
    },
    "Nantes": {
        "approved": 3,
        "rejected": 2,
        "draft": 1,
        "waiting_update": 1
    },
    "Lyon": {
        "waiting_update": 11,
        "rejected": 7,
        "approved": 3,
        "draft": 1
    },
    "Paris": {
        "rejected": 15,
        "waiting_update": 11,
        "approved": 7,
        "draft": 4
    },
    "Toulouse": {
        "waiting_update": 7,
        "rejected": 6,
        "draft": 1
    },
    "Nice": {
        "waiting_update": 4,
        "rejected": 3,
        "approved": 2,
        "draft": 1
    },
    "Nancy": {
        "rejected": 4,
        "waiting_update": 3,
        "approved": 1
    },
    "Marseille": {
        "rejected": 5,
        "waiting_update": 4,
        "approved": 1
    },
    "Montpellier": {
        "rejected": 6,
        "waiting_update": 5,
        "approved": 1,
        "draft": 1
    },
    "Bordeaux": {
        "rejected": 4,
        "waiting_update": 4,
        "approved": 1
    },
    "Rennes": {
        "waiting_update": 6,
        "approved": 3,
        "rejected": 1
    },
    "Barcelona": {
        "approved": 3,
        "waiting_update": 1
    },
    "Mulhouse": {
        "waiting_update": 2
    },
    "Berlin": {
        "waiting_update": 1
    },
    "Bruxelles": {
        "waiting_update": 1
    }
} 
,
"number_by_envisaged_type": {
    "solution": 129,
    "entrepreneurship": 41,
    "technical": 24
} 
,
"status_by_envisaged_type": {
    "technical": {
        "waiting_update": 8,
        "approved": 8,
        "rejected": 5,
        "draft": 3
    },
    "solution": {
        "waiting_update": 50,
        "rejected": 41,
        "draft": 21,
        "approved": 17
    },
    "entrepreneurship": {
        "rejected": 18,
        "waiting_update": 15,
        "approved": 4,
        "draft": 4
    }
} 
,
}
```

</details>

### 18:59 - 2024-06-24

<details>
<summary>Click for stats</summary>

```json
{
    "number_of_projects": 204,
    "number_of_projects_by_cities": {
        "Paris": 40,
        "Lyon": 25,
        "Cotonou": 19,
        "Toulouse": 16,
        "Strasbourg": 13,
        "Montpellier": 13,
        "Rennes": 11,
        "Nice": 10,
        "Marseille": 10,
        "Lille": 9,
        "Bordeaux": 9,
        "Nancy": 8,
        "Nantes": 7,
        "La R\u00e9union": 6,
        "Barcelona": 4,
        "Mulhouse": 2,
        "Berlin": 1,
        "Bruxelles": 1
    },
    "status_all_cities": {
        "waiting_update": 70,
        "rejected": 63,
        "draft": 37,
        "approved": 29,
        "pending": 5
    },
    "status_by_cities": {
        "Lyon": {
            "waiting_update": 9,
            "rejected": 7,
            "pending": 3,
            "draft": 3,
            "approved": 3
        },
        "Paris": {
            "rejected": 15,
            "waiting_update": 11,
            "draft": 7,
            "approved": 7
        },
        "Toulouse": {
            "waiting_update": 7,
            "rejected": 6,
            "draft": 3
        },
        "Rennes": {
            "waiting_update": 6,
            "approved": 3,
            "draft": 1,
            "rejected": 1
        },
        "Lille": {
            "rejected": 3,
            "approved": 2,
            "waiting_update": 2,
            "draft": 1,
            "pending": 1
        },
        "Strasbourg": {
            "rejected": 7,
            "draft": 2,
            "waiting_update": 2,
            "approved": 2
        },
        "Cotonou": {
            "draft": 17,
            "waiting_update": 1,
            "rejected": 1
        },
        "La R\u00e9union": {
            "waiting_update": 6
        },
        "Nantes": {
            "approved": 3,
            "rejected": 2,
            "draft": 1,
            "waiting_update": 1
        },
        "Nice": {
            "waiting_update": 4,
            "approved": 2,
            "rejected": 2,
            "draft": 1,
            "pending": 1
        },
        "Nancy": {
            "rejected": 4,
            "waiting_update": 3,
            "approved": 1
        },
        "Marseille": {
            "rejected": 5,
            "waiting_update": 4,
            "approved": 1
        },
        "Montpellier": {
            "rejected": 6,
            "waiting_update": 5,
            "approved": 1,
            "draft": 1
        },
        "Bordeaux": {
            "rejected": 4,
            "waiting_update": 4,
            "approved": 1
        },
        "Barcelona": {
            "approved": 3,
            "waiting_update": 1
        },
        "Mulhouse": {
            "waiting_update": 2
        },
        "Berlin": {
            "waiting_update": 1
        },
        "Bruxelles": {
            "waiting_update": 1
        }
    },
    "number_by_envisaged_type": {
        "solution": 136,
        "entrepreneurship": 42,
        "technical": 26
    },
    "status_by_envisaged_type": {
        "entrepreneurship": {
            "rejected": 18,
            "waiting_update": 14,
            "draft": 4,
            "approved": 4,
            "pending": 2
        },
        "solution": {
            "waiting_update": 48,
            "rejected": 40,
            "draft": 28,
            "approved": 17,
            "pending": 3
        },
        "technical": {
            "waiting_update": 8,
            "approved": 8,
            "draft": 5,
            "rejected": 5
        }
    }
}
```

</details>

### 09:53 - 2024-06-25

<details>
<summary>Click for stats</summary>

```json
{
    "number_of_projects": 207,
    "number_of_projects_by_cities": {
        "Paris": 41,
        "Lyon": 26,
        "Cotonou": 19,
        "Toulouse": 16,
        "Strasbourg": 13,
        "Montpellier": 13,
        "Rennes": 11,
        "Lille": 10,
        "Nice": 10,
        "Marseille": 10,
        "Bordeaux": 9,
        "Nancy": 8,
        "Nantes": 7,
        "La R\u00e9union": 6,
        "Barcelona": 4,
        "Mulhouse": 2,
        "Berlin": 1,
        "Bruxelles": 1
    },
    "status_all_cities": {
        "waiting_update": 69,
        "rejected": 63,
        "draft": 40,
        "approved": 29,
        "pending": 6
    },
    "status_by_cities": {
        "Lille": {
            "rejected": 3,
            "draft": 2,
            "approved": 2,
            "waiting_update": 2,
            "pending": 1
        },
        "Paris": {
            "rejected": 15,
            "waiting_update": 11,
            "draft": 8,
            "approved": 7
        },
        "Lyon": {
            "waiting_update": 8,
            "rejected": 7,
            "draft": 4,
            "pending": 4,
            "approved": 3
        },
        "Toulouse": {
            "waiting_update": 7,
            "rejected": 6,
            "draft": 3
        },
        "Rennes": {
            "waiting_update": 6,
            "approved": 3,
            "draft": 1,
            "rejected": 1
        },
        "Strasbourg": {
            "rejected": 7,
            "draft": 2,
            "waiting_update": 2,
            "approved": 2
        },
        "Cotonou": {
            "draft": 17,
            "waiting_update": 1,
            "rejected": 1
        },
        "La R\u00e9union": {
            "waiting_update": 6
        },
        "Nantes": {
            "approved": 3,
            "rejected": 2,
            "draft": 1,
            "waiting_update": 1
        },
        "Nice": {
            "waiting_update": 4,
            "approved": 2,
            "rejected": 2,
            "draft": 1,
            "pending": 1
        },
        "Nancy": {
            "rejected": 4,
            "waiting_update": 3,
            "approved": 1
        },
        "Marseille": {
            "rejected": 5,
            "waiting_update": 4,
            "approved": 1
        },
        "Montpellier": {
            "rejected": 6,
            "waiting_update": 5,
            "approved": 1,
            "draft": 1
        },
        "Bordeaux": {
            "rejected": 4,
            "waiting_update": 4,
            "approved": 1
        },
        "Barcelona": {
            "approved": 3,
            "waiting_update": 1
        },
        "Mulhouse": {
            "waiting_update": 2
        },
        "Berlin": {
            "waiting_update": 1
        },
        "Bruxelles": {
            "waiting_update": 1
        }
    },
    "number_by_envisaged_type": {
        "solution": 137,
        "entrepreneurship": 43,
        "technical": 27
    },
    "status_by_envisaged_type": {
        "solution": {
            "waiting_update": 48,
            "rejected": 40,
            "draft": 29,
            "approved": 17,
            "pending": 3
        },
        "technical": {
            "approved": 8,
            "waiting_update": 7,
            "draft": 6,
            "rejected": 5,
            "pending": 1
        },
        "entrepreneurship": {
            "rejected": 18,
            "waiting_update": 14,
            "draft": 5,
            "approved": 4,
            "pending": 2
        }
    },
    "number_status_by_tags": {
        "Video Games": {
            "waiting_update": 11,
            "rejected": 8,
            "draft": 7,
            "approved": 5
        },
        "Green Technologies": {
            "waiting_update": 2,
            "draft": 1
        },
        "Bioinformatics": {
            "draft": 1
        },
        "Web Development": {
            "rejected": 23,
            "waiting_update": 21,
            "draft": 12,
            "approved": 7,
            "pending": 1
        },
        "Blockchain": {
            "draft": 4,
            "rejected": 2,
            "approved": 2,
            "waiting_update": 2
        },
        "Open Source": {
            "rejected": 4,
            "approved": 4,
            "waiting_update": 3,
            "draft": 2
        },
        "Automation": {
            "waiting_update": 12,
            "rejected": 4,
            "draft": 3,
            "approved": 2,
            "pending": 1
        },
        "Esport": {
            "rejected": 2,
            "draft": 1,
            "waiting_update": 1
        },
        "Educational Technologies": {
            "waiting_update": 10,
            "rejected": 8,
            "approved": 3,
            "draft": 2,
            "pending": 1
        },
        "Collaborative Design": {
            "waiting_update": 2,
            "pending": 1,
            "rejected": 1
        },
        "Mobile Applications": {
            "waiting_update": 31,
            "rejected": 28,
            "draft": 14,
            "approved": 7,
            "pending": 2
        },
        "Streaming": {
            "approved": 2,
            "draft": 1
        },
        "HealthTech": {
            "rejected": 4,
            "waiting_update": 3,
            "approved": 3,
            "draft": 2
        },
        "Entertainment Computing": {
            "waiting_update": 6,
            "draft": 2,
            "approved": 2,
            "rejected": 1
        },
        "Cybersecurity": {
            "draft": 3,
            "approved": 3,
            "waiting_update": 2,
            "rejected": 1
        },
        "Data Management": {
            "draft": 6,
            "rejected": 5,
            "waiting_update": 1,
            "approved": 1
        },
        "Machine Learning": {
            "waiting_update": 14,
            "rejected": 9,
            "approved": 7,
            "draft": 5,
            "pending": 1
        },
        "Social Innovation": {
            "rejected": 6,
            "draft": 3,
            "approved": 3,
            "waiting_update": 2
        },
        "Tech for Good": {
            "waiting_update": 7,
            "approved": 6,
            "rejected": 3,
            "draft": 2,
            "pending": 1
        },
        "Big Data": {
            "waiting_update": 2,
            "draft": 1,
            "rejected": 1
        },
        "Data Analysis": {
            "waiting_update": 9,
            "rejected": 9,
            "draft": 5,
            "approved": 4,
            "pending": 1
        },
        "3D Modeling": {
            "draft": 4,
            "waiting_update": 2,
            "rejected": 2
        },
        "Assistive Technologies": {
            "rejected": 4,
            "draft": 2,
            "waiting_update": 2,
            "approved": 1
        },
        "Social Networks": {
            "rejected": 8,
            "waiting_update": 5,
            "draft": 1
        },
        "Voice Recognition": {
            "waiting_update": 3,
            "approved": 1
        },
        "Digital Transformation": {
            "approved": 2,
            "waiting_update": 2,
            "rejected": 1
        },
        "Geolocation": {
            "rejected": 4,
            "draft": 2,
            "waiting_update": 1,
            "approved": 1
        },
        "Product Design": {
            "waiting_update": 1,
            "rejected": 1
        },
        "Hybrid Applications": {
            "draft": 2,
            "waiting_update": 1,
            "rejected": 1
        },
        "E-commerce": {
            "waiting_update": 2,
            "rejected": 2,
            "draft": 1
        },
        "Robotics": {
            "waiting_update": 4,
            "rejected": 1
        },
        "Sharing Platforms": {
            "rejected": 4,
            "draft": 2,
            "waiting_update": 1
        },
        "Web Services": {
            "rejected": 8,
            "waiting_update": 4,
            "pending": 2,
            "draft": 1
        },
        "Management Computing": {
            "rejected": 3,
            "waiting_update": 2,
            "pending": 1,
            "approved": 1
        },
        "Knowledge Management": {
            "draft": 1,
            "waiting_update": 1
        },
        "Connected Computing": {
            "draft": 1
        },
        "Agricultural Computing": {
            "draft": 1,
            "waiting_update": 1,
            "rejected": 1,
            "pending": 1
        },
        "Project Management": {
            "rejected": 3,
            "waiting_update": 2
        },
        "AR/VR": {
            "approved": 4,
            "draft": 2,
            "waiting_update": 1,
            "rejected": 1
        },
        "Mobile Computing": {
            "rejected": 2
        },
        "Immersive Technologies": {
            "waiting_update": 2,
            "draft": 1
        },
        "Human-Machine Interaction": {
            "waiting_update": 2,
            "rejected": 2
        },
        "Smart Cities": {
            "rejected": 1
        },
        "High Performance Computing": {
            "pending": 1,
            "approved": 1
        },
        "Game Design": {
            "waiting_update": 4,
            "approved": 3,
            "rejected": 2,
            "draft": 1
        },
        "Internet of Things": {
            "waiting_update": 2
        },
        "Predictive Analytics": {
            "pending": 1,
            "rejected": 1
        },
        "DevOps": {
            "waiting_update": 3,
            "approved": 3
        },
        "FinTech": {
            "approved": 2,
            "waiting_update": 1
        },
        "Cryptocurrencies": {
            "waiting_update": 2
        },
        "Distributed Computing": {
            "approved": 1
        },
        "Signal Processing": {
            "approved": 1,
            "waiting_update": 1
        },
        "Mathematical Modeling": {
            "approved": 1,
            "waiting_update": 1
        },
        "Agile Development": {
            "waiting_update": 1,
            "rejected": 1
        },
        "Renewable Energy": {
            "waiting_update": 1
        },
        "M2M Communication": {
            "rejected": 1
        },
        "Animaux": {
            "waiting_update": 1
        }
    }
}
```

</details>

### 20:02 - 2024-06-25

<details>
<summary>Click for stats</summary>

```json
{
    "number_of_projects": 223,
    "number_of_projects_by_cities": {
        "Paris": 46,
        "Lyon": 27,
        "Cotonou": 19,
        "Toulouse": 16,
        "Strasbourg": 15,
        "Montpellier": 13,
        "Marseille": 12,
        "Lille": 12,
        "Nice": 11,
        "Rennes": 11,
        "Bordeaux": 10,
        "Nancy": 9,
        "Nantes": 8,
        "La R\u00e9union": 6,
        "Barcelona": 4,
        "Mulhouse": 2,
        "Berlin": 1,
        "Bruxelles": 1
    },
    "status_all_cities": {
        "waiting_update": 65,
        "rejected": 63,
        "draft": 57,
        "approved": 29,
        "pending": 9
    },
    "status_by_cities": {
        "Paris": {
            "rejected": 15,
            "draft": 13,
            "waiting_update": 11,
            "approved": 7
        },
        "Strasbourg": {
            "rejected": 7,
            "draft": 4,
            "waiting_update": 2,
            "approved": 2
        },
        "Nantes": {
            "approved": 3,
            "draft": 2,
            "rejected": 2,
            "waiting_update": 1
        },
        "Nancy": {
            "rejected": 4,
            "waiting_update": 3,
            "draft": 1,
            "approved": 1
        },
        "Marseille": {
            "rejected": 5,
            "waiting_update": 3,
            "draft": 2,
            "pending": 1,
            "approved": 1
        },
        "Lyon": {
            "waiting_update": 8,
            "rejected": 7,
            "draft": 5,
            "pending": 4,
            "approved": 3
        },
        "Nice": {
            "waiting_update": 4,
            "draft": 2,
            "approved": 2,
            "rejected": 2,
            "pending": 1
        },
        "Lille": {
            "draft": 4,
            "rejected": 3,
            "approved": 2,
            "pending": 2,
            "waiting_update": 1
        },
        "Bordeaux": {
            "rejected": 4,
            "waiting_update": 4,
            "draft": 1,
            "approved": 1
        },
        "Toulouse": {
            "waiting_update": 7,
            "rejected": 6,
            "draft": 3
        },
        "Rennes": {
            "waiting_update": 6,
            "approved": 3,
            "draft": 1,
            "rejected": 1
        },
        "Cotonou": {
            "draft": 17,
            "waiting_update": 1,
            "rejected": 1
        },
        "La R\u00e9union": {
            "waiting_update": 5,
            "draft": 1
        },
        "Montpellier": {
            "rejected": 6,
            "waiting_update": 4,
            "approved": 1,
            "draft": 1,
            "pending": 1
        },
        "Barcelona": {
            "approved": 3,
            "waiting_update": 1
        },
        "Mulhouse": {
            "waiting_update": 2
        },
        "Berlin": {
            "waiting_update": 1
        },
        "Bruxelles": {
            "waiting_update": 1
        }
    },
    "number_by_envisaged_type": {
        "solution": 145,
        "entrepreneurship": 48,
        "technical": 30
    },
    "status_by_envisaged_type": {
        "solution": {
            "waiting_update": 45,
            "rejected": 40,
            "draft": 38,
            "approved": 17,
            "pending": 5
        },
        "technical": {
            "draft": 8,
            "approved": 8,
            "waiting_update": 7,
            "rejected": 5,
            "pending": 2
        },
        "entrepreneurship": {
            "rejected": 18,
            "waiting_update": 13,
            "draft": 11,
            "approved": 4,
            "pending": 2
        }
    },
    "number_status_by_tags": {
        "Mobile Applications": {
            "waiting_update": 29,
            "rejected": 28,
            "draft": 20,
            "approved": 7,
            "pending": 4
        },
        "HealthTech": {
            "rejected": 4,
            "waiting_update": 3,
            "approved": 3,
            "draft": 2
        },
        "Assistive Technologies": {
            "draft": 4,
            "rejected": 4,
            "waiting_update": 2,
            "approved": 1
        },
        "Web Development": {
            "rejected": 23,
            "waiting_update": 21,
            "draft": 15,
            "approved": 7,
            "pending": 1
        },
        "Automation": {
            "waiting_update": 11,
            "draft": 4,
            "rejected": 4,
            "pending": 2,
            "approved": 2
        },
        "Collaborative Design": {
            "draft": 2,
            "waiting_update": 2,
            "pending": 1,
            "rejected": 1
        },
        "Big Data": {
            "draft": 2,
            "waiting_update": 2,
            "rejected": 1
        },
        "Project Management": {
            "rejected": 3,
            "waiting_update": 2,
            "draft": 1
        },
        "Web Services": {
            "rejected": 8,
            "draft": 4,
            "waiting_update": 4,
            "pending": 2
        },
        "Green Technologies": {
            "draft": 2,
            "waiting_update": 2
        },
        "Tech for Good": {
            "approved": 6,
            "waiting_update": 6,
            "draft": 5,
            "rejected": 3,
            "pending": 2
        },
        "Geolocation": {
            "rejected": 4,
            "draft": 3,
            "waiting_update": 1,
            "approved": 1
        },
        "DevOps": {
            "waiting_update": 3,
            "approved": 3,
            "draft": 1
        },
        "Open Source": {
            "draft": 4,
            "rejected": 4,
            "approved": 4,
            "waiting_update": 3,
            "pending": 1
        },
        "Signal Processing": {
            "draft": 1,
            "approved": 1,
            "waiting_update": 1
        },
        "Mathematical Modeling": {
            "draft": 1,
            "approved": 1,
            "waiting_update": 1
        },
        "Data Analysis": {
            "waiting_update": 9,
            "rejected": 9,
            "draft": 6,
            "approved": 4,
            "pending": 1
        },
        "Video Games": {
            "draft": 12,
            "waiting_update": 10,
            "rejected": 8,
            "approved": 5
        },
        "Game Design": {
            "draft": 3,
            "approved": 3,
            "waiting_update": 3,
            "rejected": 2
        },
        "Cloud Computing": {
            "draft": 1
        },
        "Data Management": {
            "draft": 7,
            "rejected": 5,
            "waiting_update": 1,
            "approved": 1
        },
        "M2M Communication": {
            "draft": 1,
            "rejected": 1
        },
        "Blockchain": {
            "draft": 5,
            "rejected": 2,
            "approved": 2,
            "waiting_update": 2
        },
        "Educational Technologies": {
            "waiting_update": 10,
            "rejected": 8,
            "draft": 3,
            "approved": 3,
            "pending": 1
        },
        "Social Innovation": {
            "rejected": 6,
            "draft": 4,
            "approved": 3,
            "waiting_update": 2
        },
        "Management Computing": {
            "rejected": 3,
            "draft": 2,
            "waiting_update": 2,
            "pending": 1,
            "approved": 1
        },
        "FinTech": {
            "approved": 2,
            "draft": 1,
            "waiting_update": 1
        },
        "E-commerce": {
            "draft": 2,
            "waiting_update": 2,
            "rejected": 2
        },
        "Bioinformatics": {
            "draft": 1
        },
        "Esport": {
            "rejected": 2,
            "draft": 1,
            "waiting_update": 1
        },
        "Streaming": {
            "approved": 2,
            "draft": 1
        },
        "Entertainment Computing": {
            "waiting_update": 6,
            "draft": 2,
            "approved": 2,
            "rejected": 1
        },
        "Cybersecurity": {
            "draft": 3,
            "approved": 3,
            "waiting_update": 2,
            "rejected": 1
        },
        "Machine Learning": {
            "waiting_update": 13,
            "rejected": 9,
            "approved": 7,
            "draft": 5,
            "pending": 3
        },
        "3D Modeling": {
            "draft": 4,
            "rejected": 2,
            "waiting_update": 1
        },
        "Social Networks": {
            "rejected": 8,
            "waiting_update": 5,
            "draft": 1
        },
        "Voice Recognition": {
            "waiting_update": 3,
            "approved": 1
        },
        "Digital Transformation": {
            "approved": 2,
            "waiting_update": 2,
            "rejected": 1
        },
        "Product Design": {
            "waiting_update": 1,
            "rejected": 1
        },
        "Hybrid Applications": {
            "draft": 2,
            "waiting_update": 1,
            "rejected": 1
        },
        "Robotics": {
            "waiting_update": 4,
            "rejected": 1
        },
        "Sharing Platforms": {
            "rejected": 4,
            "draft": 2,
            "waiting_update": 1
        },
        "Knowledge Management": {
            "draft": 1,
            "waiting_update": 1
        },
        "Connected Computing": {
            "draft": 1
        },
        "Agricultural Computing": {
            "draft": 1,
            "waiting_update": 1,
            "rejected": 1,
            "pending": 1
        },
        "AR/VR": {
            "approved": 4,
            "draft": 1,
            "waiting_update": 1,
            "rejected": 1
        },
        "Mobile Computing": {
            "rejected": 2
        },
        "Immersive Technologies": {
            "waiting_update": 2
        },
        "Human-Machine Interaction": {
            "waiting_update": 2,
            "rejected": 2
        },
        "Smart Cities": {
            "rejected": 1
        },
        "High Performance Computing": {
            "pending": 1,
            "approved": 1
        },
        "Internet of Things": {
            "waiting_update": 2
        },
        "Predictive Analytics": {
            "pending": 1,
            "rejected": 1
        },
        "Cryptocurrencies": {
            "waiting_update": 2
        },
        "Distributed Computing": {
            "approved": 1
        },
        "Agile Development": {
            "pending": 1,
            "rejected": 1
        },
        "Renewable Energy": {
            "waiting_update": 1
        },
        "Animaux": {
            "pending": 1
        }
    }
}
```

</details>
