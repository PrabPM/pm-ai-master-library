# PM + AI Master Library

Private, canonical study library for product management, AI/ML, interview preparation, and portfolio storytelling.

## Library at a glance

- **26 reader PDFs**
- **3,072 pages**
- **11 curriculum volumes**
- **4 interview-preparation guides**
- **10 portfolio interview briefs**
- Editable source documents retained separately from reader PDFs

Open the visual [library index](./index.html) or use the sections below.

## 1. Curriculum

1. [Foundational Mathematics for AI, ML, and LLMs, Version 2](./01-curriculum/01-ai-ml-foundations/volume-1-foundational-mathematics-primer-v2.pdf), with its [example scripts](./01-curriculum/01-ai-ml-foundations/volume-1-examples/)
2. [AI, Machine Learning, Deep Learning, and LLMs, Version 2](./01-curriculum/01-ai-ml-foundations/volume-2-ai-ml-dl-llms-pm-masterclass-v2.pdf), with its [example scripts](./01-curriculum/01-ai-ml-foundations/volume-2-examples/)
3. [Practical AI Product Manager Field Guide, Version 2](./01-curriculum/02-ai-product-management/volume-3-practical-ai-product-manager-field-guide-v2.pdf), with its [example scripts](./01-curriculum/02-ai-product-management/volume-3-examples/)
4. [Product Design Handbook, Version 2](./01-curriculum/03-product-design/volume-4-product-design-handbook-v2.pdf)
5. [SQL Handbook for Business Analysts, Version 2](./01-curriculum/04-sql-and-data/volume-5-sql-handbook-for-business-analysts-v2.pdf), with its [practice database](./01-curriculum/04-sql-and-data/payflow_practice.sql)
6. [Python Handbook for Payment Systems, Version 2](./01-curriculum/05-python-and-engineering/volume-6-python-handbook-for-payment-systems-v2.pdf), with its [runnable examples](./01-curriculum/05-python-and-engineering/volume-6-examples/)
7. [User Research and Product Discovery, Version 2](./01-curriculum/06-user-research/volume-7-user-research-and-product-discovery-v2.pdf), with its [example scripts](./01-curriculum/06-user-research/volume-7-examples/)
8. [Growth Strategy and Experimentation, Version 2](./01-curriculum/07-growth/volume-8-growth-strategy-and-experimentation-v2.pdf), with its [example scripts](./01-curriculum/07-growth/volume-8-examples/)
9. [Product Marketing and Go-to-Market, Version 2](./01-curriculum/08-product-marketing/volume-9-product-marketing-and-go-to-market-v2.pdf), with its [example scripts](./01-curriculum/08-product-marketing/volume-9-examples/)
10. [Product Analytics and Financial Analysis, Version 2](./01-curriculum/09-product-analytics/volume-10-product-analytics-and-financial-analysis-v2.pdf), with its [example scripts](./01-curriculum/09-product-analytics/volume-10-examples/)
11. [Medscape / WebMD Senior Technical PM Field Guide, Version 2](./01-curriculum/10-medscape-webmd-digital-health/volume-11-medscape-webmd-martech-and-digital-health-field-guide-v2.pdf), with its [example scripts](./01-curriculum/10-medscape-webmd-digital-health/volume-11-examples/)

### Version 2 (October 2026)

All eleven volumes were rewritten in October 2026. Each opens with a start-here page and reading paths sized to the time you have, teaches every chapter in the same order (why it matters, the idea, a worked example, common mistakes, check yourself), and ends with labs, worked cases, an interview kit, a cheat sheet, a glossary and answers.

- **Everything shown was run.** Code listings are excerpts of scripts that ship next to each PDF, and printed output is pasted from real runs. Each folder has a `run_all.sh`.
- **SQL** (Volumes 5 and 10) runs on one practice database, `01-curriculum/04-sql-and-data/payflow_practice.sql`. Load it into a scratch PostgreSQL database and every query returns the result printed on the page.
- **Examples use PayFlow**, a fictional payments company, so no real company is given invented numbers. Volume 11 is about a real ecosystem and uses a clearly fictional practice company for its worked numbers.
- **Figures** are SVG files in `05-source-documents/curriculum/volume-N-assets`.

The PDFs are built from the Markdown sources in `05-source-documents/curriculum` with [`tools/handbook-pdf`](./tools/handbook-pdf/README.md). The editions they replace are in Git history. The preserved source editions of the AI/ML material remain in `05-source-documents/curriculum/ai-ml-source-material`.

## 2. Interview preparation

- [Generic PM Interview Questions](./02-interview-preparation/01-generic-pm/generic-pm-interview-questions.pdf)
- [FAANG L4 PM Interview Prep](./02-interview-preparation/02-faang-l4/faang-l4-pm-interview-prep-2026.pdf)
- [Technical AI PM Interview Guide](./02-interview-preparation/03-technical-ai-pm/technical-ai-pm-interview-guide.pdf)
- [Paytm Work Experience Story Bank](./02-interview-preparation/04-behavioral-and-story-bank/paytm-work-experience-story-bank.pdf)

## 3. Portfolio interview briefs

- AI products: [Claude Quota Tracker](./03-portfolio-interview-briefs/ai-products/claude-quota-tracker-interview-brief.pdf), [ClauseGuard](./03-portfolio-interview-briefs/ai-products/clauseguard-interview-brief.pdf), [InsightDraft](./03-portfolio-interview-briefs/ai-products/insightdraft-interview-brief.pdf), [ML-PM Masterclass](./03-portfolio-interview-briefs/ai-products/ml-pm-masterclass-interview-brief.pdf), [Pulse Precision](./03-portfolio-interview-briefs/ai-products/pulse-precision-interview-brief.pdf), and [SignalMap](./03-portfolio-interview-briefs/ai-products/signalmap-interview-brief.pdf)
- Fintech and payments: [KYB Donut](./03-portfolio-interview-briefs/fintech-and-payments/kyb-donut-interview-brief.pdf), [Merchant Risk Scoring](./03-portfolio-interview-briefs/fintech-and-payments/merchant-risk-scoring-interview-brief.pdf), [PayCommander](./03-portfolio-interview-briefs/fintech-and-payments/paycommander-interview-brief.pdf), and [SettleIQ](./03-portfolio-interview-briefs/fintech-and-payments/settleiq-interview-brief.pdf)

## 4. Career materials

- [Prabhjot Ahluwalia PM résumé — PDF](./06-career-materials/resume/prabhjot-ahluwalia-pm-resume.pdf)
- [Prabhjot Ahluwalia PM résumé — editable Word](./06-career-materials/resume/prabhjot-ahluwalia-pm-resume.docx)

## Source preservation policy

- Final reading copies live in Sections 1-4.
- Editable Markdown and Word files live in `05-source-documents`.
- Work-experience source documents are copied without textual or structural edits.
- Desktop sources may be retired only after their repository copies are uploaded and verified byte-for-byte.
- SHA-256 checksums for all protected Desktop source documents are recorded in [`catalog/source-checksums.sha256`](./catalog/source-checksums.sha256).
- Git history is the version record; the repository intentionally contains no duplicate archive folder.

## Privacy

This repository must remain private. It contains personal interview answers, work-experience narratives, product metrics, and career-positioning material.

## Catalog

The machine-readable inventory is in [`catalog/library-manifest.csv`](./catalog/library-manifest.csv).
