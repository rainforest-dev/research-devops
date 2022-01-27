const fields = [
  "s1",
  "s2",
  "s3",
  "s4",
  "s5",
  "s6",
  "s7",
  "s8",
  "s9",
  "Ha",
  "Hb",
  "Hc",
  "La",
  "Lb",
  "Lc",
] as const;
type FieldTuple = typeof fields;
type Field = FieldTuple[number];

export { fields, FieldTuple, Field };
