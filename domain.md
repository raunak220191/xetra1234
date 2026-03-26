# Pricing Supplement / Term Sheet — Domain Knowledge

## Document Description
A pricing supplement (or final terms / term sheet) sets out the specific economic and structural terms of a securities issuance under a base prospectus or offering program. For OTC derivatives, term sheets confirm the key commercial terms of a trade.

## Document Types Covered
- **Structured Notes / MTN Pricing Supplements** — issued under EMTN/GMTN programs
- **Bond Final Terms** — under a base prospectus
- **Derivatives Term Sheets** — OTC interest rate swaps, cross-currency swaps, FX forwards, options
- **Securitization Pricing** — ABS/MBS tranches

---

## Structured Notes / Bonds

### Issuer & Program
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| issuer | Who is the issuer of the securities? | |
| guarantor | Who is the guarantor, if any? | |
| program_name | What is the name of the issuance program (e.g., EMTN Programme)? | |
| program_size | What is the maximum program size? | |
| series_number | What is the series number of this issuance? | |
| tranche_number | What is the tranche number? | |
| dealer_names | Who are the dealers or underwriters? | |

### Security Economics
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| aggregate_nominal_amount | What is the aggregate nominal (principal) amount? | |
| issue_price | What is the issue price (as percentage of nominal)? | |
| denomination | What is the minimum denomination? | |
| currency | What is the currency of the securities? | |
| issue_date | What is the issue date? | |
| maturity_date | What is the maturity (scheduled redemption) date? | |
| settlement_date | What is the settlement date? | |

### Interest / Coupon
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| interest_basis | What is the interest basis (fixed, floating, zero coupon, hybrid)? | |
| fixed_coupon_rate | What is the fixed interest rate or coupon rate? | |
| floating_rate_benchmark | What is the floating rate benchmark (SOFR, EURIBOR, SONIA, etc.)? | |
| floating_rate_margin | What is the margin or spread over the floating rate benchmark? | |
| interest_payment_dates | What are the interest payment dates? | |
| interest_commencement_date | What is the interest commencement date? | |
| day_count_fraction | What is the day count fraction (Actual/360, 30/360, Actual/Actual, etc.)? | |
| business_day_convention | What is the business day convention (Modified Following, etc.)? | |
| interest_determination_date | What is the interest determination or fixing date? | |
| rate_multiplier | Is there a rate multiplier or leverage factor? | |
| rate_cap | What is the maximum interest rate (cap)? | |
| rate_floor | What is the minimum interest rate (floor)? | |

### Redemption
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| redemption_amount | What is the final redemption amount (percentage of nominal)? | |
| early_redemption_option_issuer | Does the issuer have an early redemption (call) option? | |
| early_redemption_option_holder | Does the holder have a put option? | |
| call_dates | What are the optional redemption (call) dates? | |
| call_price | What is the call price or premium? | |
| make_whole_provision | Is there a make-whole call provision? | |
| tax_call | Is there an early redemption for tax reasons? | |

### Identifiers & Listing
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| isin | What is the ISIN (International Securities Identification Number)? | 12 characters |
| cusip | What is the CUSIP number? | 9 characters |
| common_code | What is the Common Code? | |
| cfi_code | What is the CFI code? | |
| fisn | What is the FISN? | |
| listing_exchange | On which exchange are the securities listed? | |
| clearing_system | What is the clearing system (Euroclear, Clearstream, DTC)? | |

### Legal & Regulatory
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| governing_law | What is the governing law? | |
| selling_restrictions | What are the selling restrictions (US, EEA, UK, etc.)? | |
| mifid_target_market | What is the MiFID II target market classification? | |
| priips_classification | What is the PRIIPs KID classification? | |
| risk_factors | What are the key risk factors? | |

---

## OTC Derivatives Term Sheet

### Trade Economics
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| trade_date | What is the trade date? | |
| effective_date | What is the effective (start) date? | |
| termination_date | What is the termination (maturity) date? | |
| notional_amount | What is the notional amount? | |
| notional_currency | What is the notional currency? | |

### Fixed Leg (IRS/CCS)
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| fixed_rate_payer | Who is the fixed rate payer? | |
| fixed_rate | What is the fixed rate? | |
| fixed_rate_day_count | What is the day count fraction for the fixed leg? | |
| fixed_payment_frequency | What is the payment frequency for the fixed leg? | |
| fixed_payment_dates | What are the fixed rate payment dates? | |

### Floating Leg (IRS/CCS)
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| floating_rate_payer | Who is the floating rate payer? | |
| floating_rate_option | What is the floating rate option (benchmark)? | |
| floating_rate_spread | What is the spread over the floating rate? | |
| floating_rate_day_count | What is the day count fraction for the floating leg? | |
| floating_payment_frequency | What is the payment frequency for the floating leg? | |
| floating_reset_dates | What are the floating rate reset dates? | |

### Cross-Currency Specific
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| initial_exchange | Is there an initial exchange of principal? | |
| final_exchange | Is there a final exchange of principal? | |
| initial_exchange_rate | What is the initial exchange rate? | |

### Credit & Settlement
| Field | Extraction Prompt | Notes |
|-------|-------------------|-------|
| isda_master_agreement_date | What is the date of the ISDA Master Agreement? | |
| credit_support_annex | Is there a Credit Support Annex (CSA)? | |
| calculation_agent | Who is the calculation agent? | |
| settlement_method | What is the settlement method (physical, cash, net)? | |
| business_days | What are the relevant business day centers? | |

## Extraction Rules
1. All dates in DD/MM/YYYY format
2. ISIN must be exactly 12 characters (2 letter country + 9 alphanumeric + 1 check digit)
3. CUSIP must be exactly 9 characters
4. Percentages: use % symbol (e.g., "3.750%")
5. Day count conventions must be stated exactly (Actual/360, 30/360, Actual/Actual ISDA, etc.)
6. For structured/linked notes, capture the underlying reference (index, equity, FX pair)
7. For OTC derivatives, identify ISDA definitions version (2006, 2021)
8. Business day conventions: capture exact convention name (Modified Following Business Day, etc.)
9. Notional amounts: include currency code (USD, EUR, GBP, JPY, INR)
