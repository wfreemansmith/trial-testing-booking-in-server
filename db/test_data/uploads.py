# Example of the JSON frontend receives after centre uploads XLSX
example_stage_1_response = {
  "upload": {
    "centre_id": "1234",
    "session_id": 202405,
    "part_delivery": "A",
    "test_date": "2025-04-08"
  },
  "batches": [
    {
      "batch_id": "202405-1234-IPW1",
      "component": "writing",
      "version_id": "IPW1"
    },
    {
      "batch_id": "202405-1234-IPR2",
      "component": "reading",
      "version_id": "IPR2"
    },
    {
      "batch_id": "202405-1234-IPL3",
      "component": "listening",
      "version_id": "IPL3"
    }
  ],
  "candidates": [
    {
      "candidate_number": 1001,
      "candidate_name": "Alice Smith",
      "paper_sat": "IP",
      "language_id": 1,
      "writing_version_id": "IPW1",
      "reading_version_id": "IPR2",
      "listening_version_id": "IPL3",
      "writing_batch_id": "202405-1234-IPW1",
      "reading_batch_id": "202405-1234-IPR2",
      "listening_batch_id": "202405-1234-IPL3"
    }
  ]
}

example_stage_2_upload = {
  "upload": {
    "centre_id": "1234",
    "session_id": 202405,
    "part_delivery": "A",
    "test_date": "2025-04-08"
  },
  "batches": [
    {
      "batch_id": "202405-1234-IPW1",
      "component": "writing",
      "version_id": "IPW1",
      "file_uploads": [
          {"file_name": "file.pdf"}
          ]
    },
    {
      "batch_id": "202405-1234-IPR2",
      "component": "reading",
      "version_id": "IPR2",
      "file_uploads": [
          {"file_name": "file.pdf"}
          ]
    },
    {
      "batch_id": "202405-1234-IPL3",
      "component": "listening",
      "version_id": "IPL3",
      "file_uploads": [
          {"file_name": "file.pdf"}
          ]
    }
  ],
  "candidates": [
    {
      "candidate_number": 1001,
      "candidate_name": "Alice Smith",
      "paper_sat": "IP",
      "language_id": 1,
      "writing_version_id": "IPW1",
      "reading_version_id": "IPR2",
      "listening_version_id": "IPL3",
      "writing_batch_id": "202405-1234-IPW1",
      "reading_batch_id": "202405-1234-IPR2",
      "listening_batch_id": "202405-1234-IPL3"
    }
  ]
}