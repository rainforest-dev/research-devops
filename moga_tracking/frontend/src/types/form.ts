export enum FieldType {
  String,
  Boolean,
  Number,
}

export interface Field {
  name: string;
  type: FieldType;
  validation?: () => boolean;
}
