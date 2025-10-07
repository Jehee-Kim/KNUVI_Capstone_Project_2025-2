Function AverageSkip(rng As Range, stepSize As Integer) As Double
    Dim cell As Range
    Dim i As Integer
    Dim total As Double
    Dim count As Integer

    i = 1
    For Each cell In rng
        ' stepSize마다 하나씩만 포함
        If (i - 1) Mod stepSize = 0 Then
            total = total + cell.Value
            count = count + 1
        End If
        i = i + 1
    Next cell

    If count > 0 Then
        AverageSkip = total / count
    Else
        AverageSkip = 0
    End If
End Function
