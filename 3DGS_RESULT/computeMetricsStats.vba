Sub ComputeMetricsStats()
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim i As Long, j As Long
    Dim metricCount As Integer
    Dim avgRow As Long, stdRow As Long
    Dim colStart As Integer

    Set ws = ActiveSheet
    ws.Activate

    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

    avgRow = lastRow + 2
    stdRow = avgRow + 1

    ws.Cells(avgRow, 1).Value = "Average"
    ws.Cells(stdRow, 1).Value = "Std Dev"

    metricCount = 3
    colStart = 2 

    For j = colStart To lastCol Step metricCount
        ws.Cells(avgRow, j).Value = Application.WorksheetFunction.Average(ws.Range(ws.Cells(2, j), ws.Cells(lastRow, j)))
        ws.Cells(stdRow, j).Value = Application.WorksheetFunction.StDev(ws.Range(ws.Cells(2, j), ws.Cells(lastRow, j)))

        ws.Cells(avgRow, j + 1).Value = Application.WorksheetFunction.Average(ws.Range(ws.Cells(2, j + 1), ws.Cells(lastRow, j + 1)))
        ws.Cells(stdRow, j + 1).Value = Application.WorksheetFunction.StDev(ws.Range(ws.Cells(2, j + 1), ws.Cells(lastRow, j + 1)))

        ws.Cells(avgRow, j + 2).Value = Application.WorksheetFunction.Average(ws.Range(ws.Cells(2, j + 2), ws.Cells(lastRow, j + 2)))
        ws.Cells(stdRow, j + 2).Value = Application.WorksheetFunction.StDev(ws.Range(ws.Cells(2, j + 2), ws.Cells(lastRow, j + 2)))
    Next j

    MsgBox "통계 계산 완료!", vbInformation
End Sub
