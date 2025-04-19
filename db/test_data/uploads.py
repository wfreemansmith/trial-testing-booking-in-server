# example response from initial XLSX upload
# note: maybe don't need ALL this info on the first pass??
xlsx_upload_response = {
    "upload_id": "1-3243-A", # auto-generated
    "session_id": 1,
    "centre_id": "3243",
    "part_delivery": "A",
    "epd_number": None,
    "test_date": "2025-04-10",
    "upload_date": "2025-04-19",
    "batches": [
        {
            "version_id": "ACRAP123",
            "component_id": "R",
            "file_uploads": [] # to be provided by uploader
        },
        {
            "version_id": "ACWIP1157",
            "component_id": "W",
            "file_uploads": [] # to be provided by uploader
        },
        {
            "version_id": "ACWIP1158",
            "component_id": "W",
            "file_uploads": [] # to be provided by uploader
        },
        {
            "version_id": "LBP59",
            "component_id": "L",
            "file_uploads": [] # to be provided by uploader
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
            "candidate_id": "1-3243-A-0002", # auto-generated
            "upload_id": "1-3243-A",
            "candidate_number": 2,
            "candidate_name": "Joe Santiago",
            "paper_sat": "AC",
            "writing_version": "IP1157",
            "reading_version": "AP123",
            "listening_version": "BP59"
        },
        {
            "candidate_id": "1-3243-A-0003", # auto-generated
            "upload_id": "1-3243-A",
            "candidate_number": 3,
            "candidate_name": "Alice White",
            "paper_sat": "AC",
            "writing_version": "IP1158",
            "reading_version": "AP123",
            "listening_version": "BP59"
        }
    ]
}

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