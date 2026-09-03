# Findings — Has the world decoupled growth from carbon?

One page, as the mini-project spec asks. Every figure below comes out of
[`analysis.ipynb`](./analysis.ipynb); nothing here is typed in by hand.

## What dataset did I pick, and why?

**Our World in Data's CO2 and Greenhouse Gas Emissions dataset** —
50,411 country-years, 79 columns, 1750 to 2024, released under CC BY.
<https://github.com/owid/co2-data>

Three reasons:

1. **It carries both halves of the question.** Emissions *and* GDP *and*
   population in one table means the interesting comparison is a subtraction,
   not a join against a second source I would have to reconcile.
2. **It is dirty in instructive ways.** Aggregate rows mixed in with countries,
   columns whose coverage ends in different years, a fuel breakdown that is
   93.5% missing yet still correct to use. Every cleaning decision in the
   notebook is a real decision, not a made-up exercise.
3. **It is pinnable.** The file lives in a git repository, so a commit SHA in
   the URL freezes it forever, and `fetch_data.py` checksums the download. A
   year from now this notebook produces the same numbers or it raises.

Snapshot used: commit `382ee6c`, 2026-06-02, SHA-256 `7f78e2b2...99edd5f6`.

## The single most interesting thing I found

**Absolute decoupling is real, and it is nowhere near big enough.**

Of the twenty largest emitters of 1990, **eight cut their absolute CO2 output by
2022 while growing their economies**:

| Country | CO2 1990 to 2022 | GDP 1990 to 2022 |
|---|---:|---:|
| United Kingdom | -48.3% | +73.7% |
| Germany | -36.7% | +94.0% |
| Russia | -33.9% | +103.4% |
| France | -25.2% | +63.3% |
| Italy | -22.4% | +44.8% |
| Poland | -16.3% | +296.2% |
| Japan | -10.8% | +29.0% |
| United States | -1.5% | +110.7% |

Poland is the one that should stop you: nearly a **fourfold** increase in output
against a 16% *fall* in emissions. Whatever else is true, "you cannot grow
without burning more" is not.

And then the arithmetic of the whole:

- Those eight countries removed a combined **1,999 Mt of CO2 per year**.
- China added **9,228 Mt per year** over the same period — **4.6x** every one
  of those cuts put together.
- World GDP grew **+202.4%**; world CO2 grew **+65.1%**. The carbon intensity
  of world output fell **45.4%** (0.528 to 0.288 kg CO2 per international-$)
  and total emissions still rose by two thirds, because there are far more
  dollars.

The stated finding, in one sentence:

> Eight of the twenty largest 1990 emitters cut absolute CO2 while growing GDP
> — the United Kingdom by 48.3% on 73.7% growth — but their combined 1,999
> Mt/year of cuts were outweighed 4.6 to 1 by China's 9,228 Mt/year increase,
> so global emissions rose 65.1% even as global carbon intensity fell 45.4%.

A second result worth recording, from the fuel-mix pivot: **coal's share of
world emissions fell from 60.9% in the 1950s to 36.2% in the 1970s, then climbed
back to 42.0% in the 2020s.** The "coal is finished" story is a story about
Europe and North America, not about the world.

## What I would investigate next

Swap `co2` for **`consumption_co2`** — emissions attributed to where goods are
consumed rather than where they are manufactured. That column exists in this
same dataset from 1990 onward, so it is a one-line change to the load and a
re-run of the decoupling table.

It directly tests the obvious objection to the result above: that Britain and
Germany "decarbonised" in part by importing steel, cement and electronics from
China, moving the smokestack rather than removing it. If the UK's
consumption-based cut is much smaller than its 48.3% production-based cut, the
decoupling is partly bookkeeping. If the two are close, it is real. Either
answer is worth knowing, and the data to settle it is already in `data/`.

Two smaller follow-ups:

- **Per-capita convergence.** Does the spread of `co2_per_capita` within an
  income band narrow over time? Chart 3 shows a large vertical spread at every
  income level in 2022 — France and the United States are within a factor of
  1.5 on GDP per capita and a factor of 3 apart on emissions per person. That
  gap is a policy variable, and its trend is the interesting number.
- **The bunker gap.** Summing countries misses 1,091 Mt of international
  aviation and shipping in 2023 — larger than Germany's entire national total.
  No country's inventory owns it. Worth a chart of its own.

## Charts

All four are rendered inline in the committed notebook. Running it also writes
them to `figures/`, which is produced by the run and not committed.

| File | What it shows |
|---|---|
| `figures/main.png` | Global CO2 by fuel source, 1950-2024, stacked |
| `figures/top15-total-vs-per-capita.png` | The 2023 top 15, ranked two ways |
| `figures/income-vs-carbon.png` | GDP per capita vs CO2 per capita, 2022 |
| `figures/decoupling-1990-2022.png` | Growth vs carbon for the 20 largest 1990 emitters |
