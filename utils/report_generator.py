import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

logger = logging.getLogger(__name__)

def generate_pdf_report(analysis_data: dict, output_path: str) -> str:
    """
    Generates a beautifully structured PDF placement readiness report.
    Converts metrics, skill gap, and roadmap into a professional printable PDF.
    """
    try:
        logger.info(f"Generating PDF report at: {output_path}")
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Color palette definition matching style guide (Blue & White theme)
        primary_blue = colors.HexColor("#1a73e8")
        accent_light_blue = colors.HexColor("#e8f0fe")
        dark_text_color = colors.HexColor("#202124")
        light_grey_bg = colors.HexColor("#f8f9fa")
        border_grey = colors.HexColor("#dadce0")
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=primary_blue,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#5f6368"),
            alignment=TA_CENTER
        )
        
        h1_style = ParagraphStyle(
            'SectionH1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=primary_blue,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        )
        
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=dark_text_color,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=dark_text_color
        )
        
        bullet_style = ParagraphStyle(
            'ReportBullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=dark_text_color,
            leftIndent=15,
            firstLineIndent=-10
        )
        
        table_hdr_style = ParagraphStyle(
            'TableHdr',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.white
        )
        
        table_body_style = ParagraphStyle(
            'TableBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=dark_text_color
        )

        story = []
        
        # Cover section
        story.append(Spacer(1, 30))
        story.append(Paragraph("AI CAMPUS PLACEMENT REPORT", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Preparation Analysis & Learning Roadmap for {analysis_data.get('company_name', 'Target Company')}", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Summary metrics
        resume_analysis = analysis_data.get("results", {}).get("resume_analysis", {})
        job_match = analysis_data.get("results", {}).get("job_match", {})
        
        metrics_grid_data = [
            [
                Paragraph("<b>ATS Score:</b>", body_style),
                Paragraph(f"<b>{resume_analysis.get('ats_score', 'N/A')}/100</b>", body_style),
                Paragraph("<b>Job Match Score:</b>", body_style),
                Paragraph(f"<b>{job_match.get('match_percentage', 'N/A')}%</b>", body_style)
            ]
        ]
        
        metrics_table = Table(metrics_grid_data, colWidths=[100, 100, 120, 100])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), accent_light_blue),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 1.5, primary_blue),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#b0d4ff")),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 25))
        
        # Summary block
        story.append(Paragraph("Executive Resume Summary", h1_style))
        story.append(Paragraph(resume_analysis.get("summary", "No summary available."), body_style))
        story.append(Spacer(1, 15))
        
        # Overall Recommendation
        story.append(Paragraph("Overall Recommendation", h1_style))
        story.append(Paragraph(resume_analysis.get("overall_recommendation", "No recommendation available."), body_style))
        story.append(Spacer(1, 15))
        
        story.append(PageBreak())
        
        # Resume Feedback
        story.append(Paragraph("Resume Analysis Details", h1_style))
        
        story.append(Paragraph("Strengths", h2_style))
        for strength in resume_analysis.get("strengths", []):
            story.append(Paragraph(f"&bull; {strength}", bullet_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Weaknesses / Areas of Improvement", h2_style))
        for weakness in resume_analysis.get("weaknesses", []):
            story.append(Paragraph(f"&bull; {weakness}", bullet_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Grammar & Formatting Suggestions", h2_style))
        for suggestion in resume_analysis.get("grammar_suggestions", []) + resume_analysis.get("formatting_suggestions", []):
            story.append(Paragraph(f"&bull; {suggestion}", bullet_style))
        story.append(Spacer(1, 15))
        
        # Job Match adjustments
        story.append(Paragraph("Top 5 Job Matching Adjustments", h1_style))
        for idx, change in enumerate(job_match.get("top_5_resume_changes", []), 1):
            story.append(Paragraph(f"<b>{idx}.</b> {change}", bullet_style))
            
        story.append(PageBreak())
        
        # Skill Gaps Table
        story.append(Paragraph("Skill Gap Assessment", h1_style))
        story.append(Paragraph("The table below documents critical skills required for your target role and company that were not identified in your resume. Follow the recommended learning paths and projects to build these skills.", body_style))
        story.append(Spacer(1, 10))
        
        skill_gaps = analysis_data.get("results", {}).get("skill_gap", [])
        if skill_gaps:
            gap_table_data = [
                [
                    Paragraph("Skill", table_hdr_style),
                    Paragraph("Importance", table_hdr_style),
                    Paragraph("Estimated Time", table_hdr_style),
                    Paragraph("Learning Resource & Mini-Project", table_hdr_style),
                    Paragraph("Priority", table_hdr_style)
                ]
            ]
            
            for gap in skill_gaps:
                description_str = f"<b>Resource:</b> {gap.get('learning_resource', 'N/A')}<br/><b>Project:</b> {gap.get('project_suggestion', 'N/A')}"
                gap_table_data.append([
                    Paragraph(gap.get("skill", "N/A"), table_body_style),
                    Paragraph(gap.get("importance", "N/A"), table_body_style),
                    Paragraph(gap.get("learning_time", "N/A"), table_body_style),
                    Paragraph(description_str, table_body_style),
                    Paragraph(gap.get("priority", "N/A"), table_body_style)
                ])
                
            gap_table = Table(gap_table_data, colWidths=[90, 65, 65, 220, 64])
            gap_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), primary_blue),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, border_grey),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_grey_bg])
            ]))
            story.append(gap_table)
        else:
            story.append(Paragraph("No major skill gaps identified relative to the target role.", body_style))
            
        story.append(Spacer(1, 15))
        story.append(PageBreak())
        
        # Roadmap Accordion/Timeline
        story.append(Paragraph("6-Week Learning Roadmap", h1_style))
        story.append(Paragraph("Follow this personalized study plan step-by-step over the next 6 weeks to bridge any gaps and practice for interviews.", body_style))
        story.append(Spacer(1, 10))
        
        roadmap_list = analysis_data.get("results", {}).get("learning_roadmap", [])
        for w in roadmap_list:
            w_story = [
                Paragraph(f"<b>{w.get('week', 'Week X')}</b> ({w.get('estimated_hours', 10)} Hours)", h2_style),
                Paragraph(f"<b>Topics to Cover:</b> {', '.join(w.get('topics', [])) if w.get('topics') else 'None'}", body_style),
                Paragraph(f"<b>Coding Practice:</b> {', '.join(w.get('coding_practice', [])) if w.get('coding_practice') else 'None'}", body_style),
                Paragraph(f"<b>Mini Project:</b> {', '.join(w.get('mini_projects', [])) if w.get('mini_projects') else 'None'}", body_style),
                Paragraph(f"<b>Interview Questions:</b>", body_style)
            ]
            for iq in w.get("interview_questions", []):
                w_story.append(Paragraph(f"  &bull; {iq}", bullet_style))
            w_story.append(Paragraph(f"<b>Revision Tasks:</b> {', '.join(w.get('revision_tasks', [])) if w.get('revision_tasks') else 'None'}", body_style))
            w_story.append(Spacer(1, 12))
            
            story.append(KeepTogether(w_story))
            
        doc.build(story)
        logger.info("PDF report compiled successfully.")
        return output_path
        
    except Exception as e:
        logger.error(f"Error compiling PDF report using ReportLab: {str(e)}")
        raise RuntimeError(f"ReportLab failure: {str(e)}")
