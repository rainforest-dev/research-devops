enum FieldType {
  String,
  Boolean,
  Number,
}

interface Field<T = string> {
  name: T;
  type: FieldType;
  validation?: () => boolean;
}

export { Field, FieldType };
