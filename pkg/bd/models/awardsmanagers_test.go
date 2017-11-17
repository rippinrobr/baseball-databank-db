package models


import (
  "testing"
)

func TestGetTableNameAwardsManagers(t *testing.T) {
  out := AwardsManagers{}
  expectedValue := "awardsmanagers"
  actualValue := out.GetTableName()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}

func TestGetFileNameAwardsManagers(t *testing.T) {
  out := AwardsManagers{}
  expectedValue := "AwardsManagers.csv"
  actualValue := out.GetFileName()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}

func TestGetFilePathAwardsManagers(t *testing.T) {
  out := AwardsManagers{}
  expectedValue := "/Users/robertrowe/src/baseballdatabank/core/AwardsManagers.csv"
  actualValue := out.GetFilePath()

  if actualValue != expectedValue {
    t.Errorf("actualValue (%s) != expectedValue (%s)\n", actualValue, expectedValue)
  }
}