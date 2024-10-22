# Define Swagger Template for API Metadata
swagger_template = {
    "swagger": "2.0",
    # "openapi": "3.0.0",
    "info": {
        "title": "OpenLDR API",
        "description": "This is an API for managing OPENLDR repository.",
        "version": "0.0.1",
    },
    "host": "localhost:5000",  # You can change this if running on a different host/port
    "basePath": "/",  # Base path for all endpoints
    "schemes": ["http", "https"],
    "parameters": {
        "ProvinceParameter": {
            "name": "province",
            "in": "query",
            "type": "array",
            "required": True,
            "description": "The name of the province for which to retrieve all facilities.",
            "items": {
                "type": "string",
                "enum": [
                    "Sofala",
                    "Manica",
                    "Cabo Delgado",
                    "Niassa",
                    "Maputo Provincia",
                    "Nampula",
                    "Gaza",
                    "Inhambane",
                    "Maputo Cidade",
                    "Tete",
                    "Zambezia",
                ],
            },
            "collectionFormat": "multi",
            "description": "The name(s) of the province(s) for which to retrieve all facilities. Multiple provinces can be selected.",
        },
        "DistrictParameter": {
            "name": "district",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "The name of the district to retrieve facilities from.",
            "enum": [
                "Muidumbe",
                "Palma",
                "Meluco",
                "Namuno",
                "Macomia",
                "Mecufi",
                "Pemba",
                "Quissanga",
                "Mueda",
                "Ibo",
                "Ancuabe",
                "Chiure",
                "Montepuez",
                "Nangade",
                "Metuge",
                "Balama",
                "Mocimboa da Praia",
                "Chicualacuala",
                "Chongoene",
                "Bilene Macia",
                "Mapai",
                "Chigubo",
                "Manjacaze",
                "Mabalane",
                "Limpopo",
                "Chokwe",
                "Chibuto",
                "Xai-Xai",
                "Massangena",
                "Massingir",
                "Guija",
                "Vilankulo",
                "Morrumbene",
                "Jangamo",
                "Homoine",
                "Mabote",
                "Maxixe",
                "Panda",
                "Govuro",
                "Massinga",
                "Inhambane",
                "Inhassoro",
                "Inharrime",
                "Funhalouro",
                "Zavala",
                "Guro",
                "Sussundenga",
                "Manica",
                "Mossurize",
                "Vanduzi",
                "Barue",
                "Macossa",
                "Chimoio",
                "Machaze",
                "Tambara",
                "Gondola",
                "Macate",
                "Kamaxakeni",
                "Katembe",
                "Kamavota",
                "Nlhamankulu",
                "Kanyaka",
                "KaMpfumu",
                "KaMubukwana",
                "Namaacha",
                "Manhica",
                "Boane",
                "Moamba",
                "Magude",
                "Matola",
                "Marracuene",
                "Matutuine",
                "Nacala Porto",
                "Angoche",
                "Nacala Velha",
                "Mogincual",
                "Cidade de Nampula",
                "Muecate",
                "Ribaue",
                "Liupo",
                "Monapo",
                "Nacaroa",
                "Larde",
                "Mecuburi",
                "Malema",
                "Memba",
                "Namapa-Erati",
                "Moma",
                "Mossuril",
                "Murrupula",
                "Lalaua",
                "Mogovolas",
                "Ilha de Mocambique",
                "Meconta",
                "Rapale",
                "Lago",
                "Mecanhelas",
                "Majune",
                "Muembe",
                "Nipepe",
                "Mecula",
                "Ngauma",
                "Chimbonila",
                "Marrupa",
                "Cidade de Lichinga",
                "Cuamba",
                "Metarica",
                "Mavago",
                "Maua",
                "Sanga",
                "Mandimba",
                "Nhamatanda",
                "Dondo",
                "Chemba",
                "Cheringoma",
                "Buzi",
                "Beira",
                "Chibabava",
                "Gorongoza",
                "Muanza",
                "Maringue",
                "Marromeu",
                "Machanga",
                "Caia",
                "Mutarara",
                "Tsangano",
                "Moatize",
                "Zumbo",
                "Angonia",
                "Changara",
                "Cahora Bassa",
                "Maravia",
                "Magoe",
                "Tete",
                "Doa",
                "Chifunde",
                "Macanga",
                "Marara",
                "Chiuta",
                "Derre",
                "Inhassunge",
                "Lugela",
                "Gurue",
                "Alto Molocue",
                "Maganja da Costa",
                "Nicoadala",
                "Morrumbala",
                "Molumbo",
                "Luabo",
                "Gile",
                "Mopeia",
                "Pebane",
                "Milange",
                "Ile",
                "Namarroi",
                "Namacurra",
                "Mocuba",
                "Quelimane",
                "Mulevala",
                "Chinde",
                "Mocubela",
            ],
        },
        "LabTypeParameter": {
            "name": "lab_type",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "The type of laboratory to filter by (optional).",
            "enum": [
                "Clinical Only",
                "Cytology",
                "Data Repository",
                "Environmental",
                "General",
                "Histology",
                "Point of care",
                "Postmortem",
                "TB",
                "Trials",
                "VL/EID",
            ],
        },
    },
    "components": {
        "schemas": {
            "Facilities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "FacilityName": {"type": "string"},
                        "FacilityCode": {"type": "string"},
                        "FacilityType": {"type": "string"},
                        "FacilityNationalCode": {"type": "string"},
                        "ProvinceName": {"type": "string"},
                        "DistrictName": {"type": "string"},
                        "HFStatus": {"type": "integer"},
                        "Latitude": {"type": "string"},
                        "Longitude": {"type": "string"},
                    },
                },
            },
        }
    },
}
