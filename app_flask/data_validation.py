from datetime import datetime, timedelta


# NOTE ensure json schema is valid DURING storage of data, and not retrieval

# YYYY-MM-DD limit our hist data for up to 25 yrs
history_start = (datetime.now() - timedelta(days=365.25 * 25)).strftime("%Y-%m-%d")

# TODO normalize date patterns
base_json_schema = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "last_updated": {
      "type": "string"
    },
    "source": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "url": {
          "type": "string",
          "format": "uri"
        }
      },
      "required": ["name", "url"]
    },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "date": {
            "type": "string"
          },
          "data": {
            "type": "object"
          }
        },
        "required": ["date", "data"]
      }
    }
  },
  "required": ["last_updated", "source", "entries"]
}
"""


# base_json_schema = """
# {
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "type": "object",
#   "properties": {
#     "last_updated": {
#       "type": "string",
#       "format": "date-time"
#     },
#     "source": {
#       "type": "object",
#       "properties": {
#         "name": {
#           "type": "string"
#         },
#         "url": {
#           "type": "string",
#           "format": "uri"
#         }
#       },
#       "required": ["name", "url"]
#     },
#     "entries": {
#       "type": "array",
#       "items": {
#         "type": "object",
#         "properties": {
#           "date": {
#             "type": "string",
#             "format": "date"
#           },
#           "data": {
#             "type": "object"
#             // You can define properties for the data object if needed
#           }
#         },
#         "required": ["date", "data"]
#       }
#     }
#   },
#   "required": ["last_updated", "source", "entries"]
# }  
# """