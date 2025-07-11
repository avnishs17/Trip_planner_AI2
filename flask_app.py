from flask import Flask, render_template, request, jsonify
import requests
import datetime
import os
import re
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')



def process_ai_response(text):
    """Process AI response text to proper HTML format with full markdown support"""
    
    # Split text into lines for processing
    lines = text.split('\n')
    processed_lines = []
    in_table = False
    in_list = False
    table_headers = []
    list_type = None  # 'ul' for unordered, 'ol' for ordered
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines but preserve spacing
        if not line:
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            processed_lines.append('')
            i += 1
            continue
        
        # Handle headers (must be at start of line)
        if line.startswith('####'):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            header_text = line[4:].strip()
            processed_lines.append(f'<h4>{header_text}</h4>')
        elif line.startswith('###'):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            header_text = line[3:].strip()
            processed_lines.append(f'<h3>{header_text}</h3>')
        elif line.startswith('##'):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            header_text = line[2:].strip()
            processed_lines.append(f'<h2>{header_text}</h2>')
        elif line.startswith('#'):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            header_text = line[1:].strip()
            processed_lines.append(f'<h1>{header_text}</h1>')
        
        # Handle horizontal rules
        elif line.strip() == '---' or line.strip() == '***':
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            processed_lines.append('<hr>')
        
        # Handle tables
        elif '|' in line and line.count('|') >= 2:
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            
            # Check if this is a header separator line (like |---|---|)
            if re.match(r'^[\s\|:\-]+$', line):
                # This is a separator line, skip it
                i += 1
                continue
            
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')]
            # Remove empty cells from start and end (common in markdown tables)
            while cells and not cells[0]:
                cells.pop(0)
            while cells and not cells[-1]:
                cells.pop()
            
            if cells:
                if not in_table:
                    processed_lines.append('<table class="table table-striped table-bordered">')
                    in_table = True
                    table_headers = cells
                    # Create header row
                    processed_lines.append('<thead><tr>')
                    for cell in cells:
                        processed_lines.append(f'<th>{process_inline_formatting(cell)}</th>')
                    processed_lines.append('</tr></thead><tbody>')
                else:
                    # Create data row
                    processed_lines.append('<tr>')
                    for cell in cells:
                        processed_lines.append(f'<td>{process_inline_formatting(cell)}</td>')
                    processed_lines.append('</tr>')
        
        # Handle unordered lists (- or *)
        elif line.startswith('- ') or line.startswith('* '):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            
            list_content = line[2:].strip()
            if not in_list or list_type != 'ul':
                if in_list:
                    processed_lines.append(f'</{list_type}>')
                processed_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            processed_lines.append(f'<li>{process_inline_formatting(list_content)}</li>')
        
        # Handle ordered lists (1. 2. 3. etc.)
        elif re.match(r'^\d+\.\s', line):
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            
            list_content = re.sub(r'^\d+\.\s', '', line)
            if not in_list or list_type != 'ol':
                if in_list:
                    processed_lines.append(f'</{list_type}>')
                processed_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            processed_lines.append(f'<li>{process_inline_formatting(list_content)}</li>')
        
        # Handle regular paragraphs
        else:
            if in_table:
                processed_lines.append('</table>')
                in_table = False
            if in_list:
                processed_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            
            # Check if this is a bold text that should be a header
            header_level = detect_header_from_bold(line)
            if header_level:
                # Extract text from **text** and make it a header
                header_text = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
                processed_lines.append(f'<h{header_level}>{header_text}</h{header_level}>')
            else:
                # Process regular paragraph
                processed_lines.append(f'<p>{process_inline_formatting(line)}</p>')
        
        i += 1
    
    # Close any open tags
    if in_table:
        processed_lines.append('</tbody></table>')
    if in_list:
        processed_lines.append(f'</{list_type}>')
    
    # Join all lines and clean up
    html_content = '\n'.join(processed_lines)
    
    # Clean up excessive whitespace
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    
    return html_content

def detect_header_from_bold(line):
    """Detect if a bold text line should be treated as a header and return appropriate level"""
    if not line or not line.strip():
        return None
    
    # Check if the entire line is just bold text (likely a header)
    bold_pattern = r'^\*\*(.*?)\*\*$'
    if re.match(bold_pattern, line.strip()):
        header_text = re.sub(bold_pattern, r'\1', line.strip()).strip()
        
        # Determine header level based on content and context
        header_keywords = {
            # Main section headers (h2)
            2: ['overview', 'itinerary', 'accommodation', 'dining', 'transportation', 
                'activities', 'attractions', 'cost breakdown', 'practical information',
                'destination overview', 'itinerary plans', 'accommodation recommendations',
                'dining guide', 'transportation details', 'comprehensive cost breakdown'],
            
            # Sub-section headers (h3)
            3: ['plan a', 'plan b', 'popular tourist route', 'off-the-beaten-path',
                'budget option', 'luxury option', 'popular restaurants', 'local eateries',
                'budget breakdown', 'daily schedule'],
            
            # Day/detail headers (h4)
            4: ['day 1', 'day 2', 'day 3', 'day 4', 'day 5', 'day 6', 'day 7',
                'morning', 'afternoon', 'evening', 'breakfast', 'lunch', 'dinner']
        }
        
        header_lower = header_text.lower()
        
        # Check for day patterns first (highest priority for h4)
        if re.search(r'day \d+', header_lower) or header_lower in ['morning', 'afternoon', 'evening']:
            return 4
        
        # Check other keywords by level
        for level, keywords in header_keywords.items():
            for keyword in keywords:
                if keyword in header_lower:
                    return level
        
        # If it's a short line (likely a header) but doesn't match keywords, default to h3
        if len(header_text) < 50 and ':' in header_text:
            return 3
        elif len(header_text) < 30:
            return 3
    
    return None

def process_inline_formatting(text):
    """Process inline markdown formatting like bold, italics, etc."""
    if not text:
        return text
    
    # Handle bold text: **text** -> <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Handle italics: *text* -> <em>text</em> (but avoid conflicting with bold)
    text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Handle inline code: `code` -> <code>code</code>
    text = re.sub(r'`([^`]+?)`', r'<code>\1</code>', text)
    
    # Fix any malformed HTML tags from AI
    text = re.sub(r'<strong>(.*?)<strong>', r'<strong>\1</strong>', text)
    text = re.sub(r'<em>(.*?)<em>', r'<em>\1</em>', text)
    
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page for the travel planner - handles both form display and results"""
    if request.method == 'GET':
        return render_template('index.html')
    
    # Handle POST request (form submission)
    try:
        user_input = request.form.get('question', '').strip()
        
        if not user_input:
            return render_template('index.html', error='Please enter a valid travel query.')
        
        # Call the backend API
        payload = {"question": user_input}
        response = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer returned.")
            saved_file = data.get("saved_file", "")
            
            # Process the answer using our improved function
            processed_answer = process_ai_response(answer)
            
            return render_template('index.html', 
                                 answer=processed_answer, 
                                 question=user_input,
                                 saved_file=saved_file,
                                 show_results=True,
                                 timestamp=datetime.datetime.now().strftime('%Y-%m-%d at %H:%M'))
        else:
            return render_template('index.html', error=f'Backend API error: {response.text}')
            
    except requests.exceptions.Timeout:
        return render_template('index.html', error='Request timed out. Please try again.')
    except requests.exceptions.ConnectionError:
        return render_template('index.html', error='Could not connect to the backend service. Please ensure it is running.')
    except Exception as e:
        logger.error(f"Error in index: {str(e)}")
        return render_template('index.html', error=f'An error occurred: {str(e)}')

@app.route('/api/plan', methods=['POST'])
def api_plan_trip():
    """API endpoint for trip planning (for AJAX requests)"""
    try:
        data = request.get_json()
        user_input = data.get('question', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Please provide a valid travel query.'}), 400
        
        # Call the backend API
        payload = {"question": user_input}
        response = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "No answer returned.")
            
            # Process the answer using our improved function
            processed_answer = process_ai_response(answer)
            
            return jsonify({
                'success': True,
                'answer': processed_answer,
                'saved_file': result.get("saved_file", ""),
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')
            })
        else:
            return jsonify({'error': f'Backend API error: {response.text}'}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Could not connect to the backend service.'}), 503
    except Exception as e:
        logger.error(f"Error in api_plan_trip: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if backend is accessible
        response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
        backend_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        backend_status = "unreachable"
    
    return jsonify({
        'status': 'healthy',
        'backend_status': backend_status,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
