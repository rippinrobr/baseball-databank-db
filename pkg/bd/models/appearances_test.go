package models


import (
  "testing"
)

func TestGetTableNameAppearances(t *testing.T) {
  out := Appearances{}
  expectedValue := "appearances"
  actualValue := out.GetTableName()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}

func TestGetFileNameAppearances(t *testing.T) {
  out := Appearances{}
  expectedValue := "Appearances.csv"
  actualValue := out.GetFileName()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}

func TestGetFilePathAppearances(t *testing.T) {
  out := Appearances{}
  expectedValue := "/Users/robertrowe/src/baseballdatabank/core/Appearances.csv"
  actualValue := out.GetFilePath()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}