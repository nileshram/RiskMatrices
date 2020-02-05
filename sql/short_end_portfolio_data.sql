select con.Product, con.ExpirationDate as ExpiryDate, con.Symbol, con.Strike, con.PutCall, con.Name, pos.[Position], calc.Theo, calc.Delta, calc.Gamma,
calc.Theta, calc.Vega, calc.ImpliedVolatility, calc.ActualVolatility, calc.TimeToExpiry
from Abn.dbo.Contracts as con
left outer join Abn.dbo.Positions as pos on pos.FkContractId = con.Id
left outer join [Act-Arc].dbo.Calculations as calc on con.Id = calc.FkContractId
where pos.[Position] is not null and calc.Theo is not null
order by con.ExpirationDate desc;