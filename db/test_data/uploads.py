# example response from initial XLSX upload
expected_xlsx_res_1 = [
    {
        "filename": "test_register_1",
        "centre_num": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "errors": []
            }
        ],
        "candidates": [
            {
                "candidate_number": 1,
                "candidate_name": "Mary Bloggs",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                #"writing_version_id": "ACWIP1157",
                "reading_version": "AP123",
                #"reading_version_id": "ACRAP123",
                "listening_version": "BP59",
                #"listening_version_id": "LBP59",
                "errors": []
            },
            {
                "candidate_number": 2,
                "candidate_name": "Joe Santiago",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                #"writing_version_id": "ACWIP1157",
                "reading_version": "AP123",
                #"reading_version_id": "ACRAP123",
                "listening_version": "BP59",
                #"listening_version_id": "LBP59",
                "errors": []
            },
            {
                "candidate_number": 3,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                #"writing_version_id": "ACWIP1158",
                "reading_version": "AP123",
                #"reading_version_id": "ACRAP123",
                "listening_version": "BP59",
                #"listening_version_id": "LBP59",
                "errors": []
            }
        ],
        "errors": []
    },
    {
        "filename": "test_register_2",
        "centre_num": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "errors": []
            },
            {
                "version_id": "GTRCP54",
                "component_id": "R",
                "errors": []
            },
            {
                "version_id": "GTWAP476",
                "component_id": "W",
                "errors": []
            },
            {
                "version_id": "LBP23",
                "component_id": "L",
                "errors": []
            },
             {
                "version_id": "LBP59",
                "component_id": "L",
                "errors": []
            }
        ],
        "candidates": [
            {
                "candidate_number": 1,
                "candidate_name": "Mary Bloggs",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            },
            {
                "candidate_number": 2,
                "candidate_name": "Joe Santiago",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            },
            {
                "candidate_number": 3,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            },
            {
                "candidate_number": 4,
                "candidate_name": "Bingo Radical",
                "paper_sat": "GT",
                "writing_version": None,
                "reading_version": "CP54",
                "listening_version": None,
                "errors": []
            },
            {
                "candidate_number": 5,
                "candidate_name": "Dave McFiggins",
                "paper_sat": "GT",
                "writing_version": "AP476",
                "reading_version": "CP54",
                "listening_version": "BP23",
                "errors": []
            },
            {
                "candidate_number": 6,
                "candidate_name": "Gusto McGee",
                "paper_sat": "GT",
                "writing_version": "AP476",
                "reading_version": "CP54",
                "listening_version": "BP23",
                "errors": []
            },
            {
                "candidate_number": 8,
                "candidate_name": "Sandra Pollock",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            }
        ],
        "errors": []
    }
]

# example upload received by the API
# same as above but all auto-generated fields removed, should generate the same
complete_upload_send_json = {
    "session_id": 1,
    "centre_id": "3243",
    "epd_number": None,
    "test_date": "2025-04-10",
    "batches": [
        {
            "version_id": "ACRAP123",
            "component_id": "R",
            "file_uploads": [
                {
                    "file_name": "READING_SCANS_AP123.pdf"
                }
            ]
        },
        {
            "version_id": "ACWIP1157",
            "component_id": "W",
            "file_uploads": [
                {
                    "file_name": "WRITING_SCANS_IP1157.pdf"
                }
            ]
        },
        {
            "version_id": "ACWIP1158",
            "component_id": "W",
            "file_uploads": [
                {
                    "file_name": "WRITING_SCANS_IP1158.pdf"
                }
            ]
        },
        {
            "version_id": "LBP59",
            "component_id": "L",
            "file_uploads": [
                {
                    "file_name": "LISTENING_SCANS_BP59.pdf"
                }
            ] 
        }
    ],
    "candidates": [
        {
            "candidate_number": 1,
            "candidate_name": "Mary Bloggs",
            "paper_sat": "AC",
            "writing_version": "IP1157",
            "reading_version": "AP123",
            "listening_version": "BP59"
        },
        {
            "candidate_number": 2,
            "candidate_name": "Joe Santiago",
            "paper_sat": "AC",
            "writing_version": "IP1157",
            "reading_version": "AP123",
            "listening_version": "BP59"
        },
        {
            "candidate_number": 3,
            "candidate_name": "Alice White",
            "paper_sat": "AC",
            "writing_version": "IP1158",
            "reading_version": "AP123",
            "listening_version": "BP59"
        }
    ]
}