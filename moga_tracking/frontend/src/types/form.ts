export enum FieldType {
  String,
  Boolean,
  Number,
}

export interface Field<T = string> {
  name: T;
  type: FieldType;
  validation?: () => boolean;
}
