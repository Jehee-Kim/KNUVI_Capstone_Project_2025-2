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

Sub GenerateMetricSummary()
    Dim ws As Worksheet
    Dim summaryWs As Worksheet
    Dim chartObj As ChartObject
    Dim lastRow As Long, lastCol As Long
    Dim avgRow As Long
    Dim i As Long, metricName As String
    Dim rngAvg As Range
    
    Set ws = ActiveSheet
    
    On Error Resume Next
    Application.DisplayAlerts = False
    Worksheets("Summary").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0
    

    Set summaryWs = Worksheets.Add
    summaryWs.Name = "Summary"
    
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    For i = 1 To lastRow
        If ws.Cells(i, 1).Value = "Average" Then
            avgRow = i
            Exit For
        End If
    Next i
    
    If avgRow = 0 Then
        MsgBox "먼저 ComputeMetricsStats를 실행해주세요!", vbExclamation
        Exit Sub
    End If
    
    ws.Rows(avgRow).Copy Destination:=summaryWs.Range("A1")
    
    summaryWs.Cells(1, 1).Value = "Metric Summary"
    summaryWs.Cells(2, 1).Value = "PSNR"
    summaryWs.Cells(3, 1).Value = "SSIM"
    summaryWs.Cells(4, 1).Value = "LPIPS"
    
    summaryWs.Cells(2, 2).Value = ws.Cells(avgRow, 2).Value
    summaryWs.Cells(3, 2).Value = ws.Cells(avgRow, 3).Value
    summaryWs.Cells(4, 2).Value = ws.Cells(avgRow, 4).Value
   
    Set chartObj = summaryWs.ChartObjects.Add(Left:=250, Top:=20, Width:=400, Height:=250)
    chartObj.Chart.SetSourceData Source:=summaryWs.Range("A2:B4")
    chartObj.Chart.ChartType = xlColumnClustered
    chartObj.Chart.ChartTitle.Text = "Average Metric Comparison"
    chartObj.Chart.Axes(xlValue).HasTitle = True
    chartObj.Chart.Axes(xlValue).AxisTitle.Text = "Score"
    
    MsgBox "요약 리포트 생성 완료!", vbInformation
End Sub

