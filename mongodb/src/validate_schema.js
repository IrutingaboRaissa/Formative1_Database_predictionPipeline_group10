// In mongosh:
// use student_performance_db
// Then run:

db.runCommand({
  collMod: "students",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["gender", "math_score", "reading_score", "writing_score", "created_at"],
      properties: {
        gender: { bsonType: "string", description: "must be a string" },
        race: { bsonType: ["string", "null"] },
        parent_education: { bsonType: ["string", "null"] },
        lunch: { bsonType: ["string", "null"] },
        test_prep_course: { bsonType: ["string", "null"] },
        math_score: { bsonType: "number", minimum: 0, maximum: 100 },
        reading_score: { bsonType: "number", minimum: 0, maximum: 100 },
        writing_score: { bsonType: "number", minimum: 0, maximum: 100 },
        created_at: { bsonType: "date" }
      },
      additionalProperties: true
    }
  },
  validationLevel: "moderate",
  validationAction: "warn" // change to "error" to block invalid writes
})
