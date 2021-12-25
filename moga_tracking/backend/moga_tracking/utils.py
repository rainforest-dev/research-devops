def is_float(element: str) -> bool:
  try:
    float(element)
    return True
  except ValueError:
    return False
