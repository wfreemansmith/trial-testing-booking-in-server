from datetime import date, timedelta

# input files + expected responses to upload/preview
upload_preview_expected_res = [
    {
        "filename": "test_register_1",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
            }
        ],
        "errors": []
    },
    {
        "filename": "test_register_2",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTRCP54",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTWAP476",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP23",
                "component_id": "L",
                "file_uploads": [],
                "errors": []
            },
             {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
    },
    {
        "filename": "test_register_3",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
                "errors": [
                    {
                        'field': 'candidate_number',
                        'message': 'Candidate number cannot be duplicated, please use a unique candidate number.'
                    }
                ]
            },
            {
                "candidate_number": 2,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        'field': 'candidate_number',
                        'message': 'Candidate number cannot be duplicated, please use a unique candidate number.'
                    }
                ]
            },
            {
                "candidate_number": 3,
                "candidate_name": "Giovani Miranda",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            }
        ],
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    },
    {
        "filename": "test_register_4",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTRCP54",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTWAP476",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP23",
                "component_id": "L",
                "file_uploads": [],
                "errors": []
            },
             {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
                "paper_sat": None,
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "paper_sat",
                        "message": "Please enter 'AC' or 'GT' for this candidate."
                    }
                ]
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
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    },
    {
        "filename": "test_register_5",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTRCP54",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
             {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
                "candidate_name": "Mary Bloggs",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            },
            {
                "candidate_number": 3,
                "candidate_name": "Alice White",
                "paper_sat": None,
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "paper_sat",
                        "message": "Please enter 'AC' or 'GT' for this candidate."
                    }
                ]
            },
            {
                "candidate_number": 4,
                "candidate_name": "Alice White",
                "paper_sat": "GT",
                "writing_version": None,
                "reading_version": "CP54",
                "listening_version": None,
                "errors": []
            }
        ],
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    },
    {
        "filename": "test_register_6",
        "centre_id": "3243",
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "GTRCP54",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
             {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
                "errors": [
                    {
                        'field': 'candidate_number',
                        'message': 'Candidate number cannot be duplicated, please use a unique candidate number.'
                    }
                ]
            },
            {
                "candidate_number": 2,
                "candidate_name": "Mary Bloggs",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": []
            },
            {
                "candidate_number": 3,
                "candidate_name": "Alice White",
                "paper_sat": None,
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "paper_sat",
                        "message": "Please enter 'AC' or 'GT' for this candidate."
                    }
                ]
            },
            {
                "candidate_number": 1,
                "candidate_name": "David Muffin",
                "paper_sat": "GT",
                "writing_version": None,
                "reading_version": "CP54",
                "listening_version": None,
                "errors": [
                    {
                        'field': 'candidate_number',
                        'message': 'Candidate number cannot be duplicated, please use a unique candidate number.'
                    }
                ]
            }
        ],
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    }
]

# inputs for upload/refresh
upload_refresh_inputs = [
    {
        "TEST_ID": "input_1 - no issues",
        "marking_window_id": 1,
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
                "file_uploads": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [] 
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
    },
    {
        "TEST_ID": "input_2 - missing cand data",
        "marking_window_id": 1,
        "centre_id": "3243",
        "epd_number": None,
        "test_date": None,
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
                "candidate_name": None,
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59"
            },
            {
                "candidate_number": 2,
                "candidate_name": "",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59"
            },
            {
                "candidate_number": None,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59"
            }
        ]
    },
    {
        "TEST_ID": "input_3 - date in future",
        "marking_window_id": 1,
        "centre_id": "3243",
        "epd_number": None,
        "test_date": (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
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
                        "file_name": "WRITING SCANS.pdf"
                    }
                ]
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [] 
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
            }
        ]
    }
]

# expected responses for upload/refresh
upload_refresh_expected_responses = [
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [
                    {
                        "file_name": "READING_SCANS_AP123.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
            }
        ],
        "errors": []
    },
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [
                    {
                        "file_name": "READING_SCANS_AP123.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING_SCANS_IP1157.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING_SCANS_IP1158.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [
                    {
                        "file_name": "LISTENING_SCANS_BP59.pdf"
                    }
                ],
                "errors": []
            }
        ],
        "candidates": [
            {
                "candidate_number": 1,
                "candidate_name": None,
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_name",
                        "message": "Candidate name cannot be blank. Please provide a name for the candidate."
                    }
                ]
            },
            {
                "candidate_number": 2,
                "candidate_name": "",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_name",
                        "message": "Candidate name cannot be blank. Please provide a name for the candidate."
                    }
                ]
            },
            {
                "candidate_number": None,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_number",
                        "message": "Candidate number cannot be blank or zero. Please provide a candidate number that you have not used previously."
                    }
                ]
            }
        ],
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    },
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [
                    {
                        "file_name": "READING_SCANS_AP123.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING SCANS.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
            }
        ],
        "errors": [
            {
                "field": "test_date",
                "message": "Date cannot be in the future."
            }
        ]
    }
]

upload_submit_expected_responses = [
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
            }
        ],
        "errors": []
    },
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [
                    {
                        "file_name": "READING_SCANS_AP123.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING_SCANS_IP1157.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1158",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING_SCANS_IP1158.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [
                    {
                        "file_name": "LISTENING_SCANS_BP59.pdf"
                    }
                ],
                "errors": []
            }
        ],
        "candidates": [
            {
                "candidate_number": 1,
                "candidate_name": None,
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_name",
                        "message": "Candidate name cannot be blank. Please provide a name for the candidate."
                    }
                ]
            },
            {
                "candidate_number": 2,
                "candidate_name": "",
                "paper_sat": "AC",
                "writing_version": "IP1157",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_name",
                        "message": "Candidate name cannot be blank. Please provide a name for the candidate."
                    }
                ]
            },
            {
                "candidate_number": None,
                "candidate_name": "Alice White",
                "paper_sat": "AC",
                "writing_version": "IP1158",
                "reading_version": "AP123",
                "listening_version": "BP59",
                "errors": [
                    {
                        "field": "candidate_number",
                        "message": "Candidate number cannot be blank or zero. Please provide a candidate number that you have not used previously."
                    }
                ]
            }
        ],
        "errors": [
            {
                "field": "candidates",
                "message": "There was an error with one or more candidates."
            }
        ]
    },
    {
        "batches": [
            {
                "version_id": "ACRAP123",
                "component_id": "R",
                "file_uploads": [
                    {
                        "file_name": "READING_SCANS_AP123.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "ACWIP1157",
                "component_id": "W",
                "file_uploads": [
                    {
                        "file_name": "WRITING SCANS.pdf"
                    }
                ],
                "errors": []
            },
            {
                "version_id": "LBP59",
                "component_id": "L",
                "file_uploads": [],
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
            }
        ],
        "errors": [
            {
                "field": "test_date",
                "message": "Date cannot be in the future."
            }
        ]
    }
]

# example upload received by the API - for testing the DAO
complete_upload_json = [
    {
        "marking_window_id": 1,
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
]