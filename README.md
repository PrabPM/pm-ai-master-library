# PM + AI Master Library

Private, canonical study library for product management, AI/ML, interview preparation, and portfolio storytelling.

## Library at a glance

- **26 reader PDFs**
- **2,963 pages**
- **11 curriculum volumes**
- **4 interview-preparation guides**
- **10 portfolio interview briefs**
- Editable source documents retained separately from reader PDFs

Open the visual [library index](./index.html) or use the sections below.

## 1. Curriculum

1. [Foundational Mathematics for AI, ML, and LLMs](./01-curriculum/01-ai-ml-foundations/volume-1-foundational-mathematics-primer.pdf)
2. [AI, Machine Learning, Deep Learning, and LLMs](./01-curriculum/01-ai-ml-foundations/volume-2-ai-ml-dl-llms-pm-masterclass-expanded.pdf)
3. [Practical AI Product Manager Field Guide](./01-curriculum/02-ai-product-management/volume-3-practical-ai-product-manager-field-guide-july-2026.pdf)
4. [Product Design Handbook, Version 2](./01-curriculum/03-product-design/volume-4-product-design-handbook-v2.pdf)
5. [SQL Handbook for Business Analysts, Version 2](./01-curriculum/04-sql-and-data/volume-5-sql-handbook-for-business-analysts-v2.pdf), with its [practice database](./01-curriculum/04-sql-and-data/payflow_practice.sql)
6. [Python Handbook for Payment Systems, Version 2](./01-curriculum/05-python-and-engineering/volume-6-python-handbook-for-payment-systems-v2.pdf), with its [runnable examples](./01-curriculum/05-python-and-engineering/volume-6-examples/)
7. [User Research and Product Discovery](./01-curriculum/06-user-research/volume-7-user-research-and-product-discovery-july-2026.pdf)
8. [Growth Strategy and Experimentation](./01-curriculum/07-growth/volume-8-growth-strategy-and-experimentation-july-2026.pdf)
9. [Product Marketing and Go-to-Market](./01-curriculum/08-product-marketing/volume-9-product-marketing-and-go-to-market-july-2026.pdf)
10. [Product Analytics and Financial Analysis](./01-curriculum/09-product-analytics/volume-10-product-analytics-and-financial-analysis-july-2026.pdf)
11. [Medscape / WebMD Senior Technical PM Field Guide](./01-curriculum/10-medscape-webmd-digital-health/volume-11-medscape-webmd-martech-and-digital-health-field-guide-july-2026.pdf)

Volumes 1-3 retain their original canonical pages and add labeled source-preservation appendices. Exact source editions remain in `05-source-documents/curriculum/ai-ml-source-material`.

### Version 2 handbooks (Volumes 4-6)

The three handbooks were recomposed in October 2026. Each now opens with a start-here page and three reading paths, teaches every chapter in the same order (why it matters, the idea, a worked example, common mistakes, check yourself), and ends with labs, worked cases, an interview kit, a cheat sheet, a glossary and answers.

- **Product Design** has 13 wireframe figures; their sources are in `05-source-documents/curriculum/volume-4-assets`.
- **SQL** runs on one practice database. Load `payflow_practice.sql` into a scratch PostgreSQL database and every query in the book returns the result printed on the page.
- **Python** ships a folder of runnable examples, one per chapter. `./volume-6-examples/run_all.sh` runs them all and the test suite.

The PDFs are built from the Markdown sources in `05-source-documents/curriculum` with [`tools/handbook-pdf`](./tools/handbook-pdf/README.md). The July 2026 editions they replace are in Git history.

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
