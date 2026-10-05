-- Database Schema & Seeds for Drug Prevention & Community Support System
-- Target Database: SQLite 3

PRAGMA foreign_keys = ON;

-- 1. Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER', -- 'USER', 'CONSULTANT', 'ADMIN'
    phone VARCHAR(20),
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Consultants table
CREATE TABLE IF NOT EXISTS consultants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    bio TEXT,
    qualifications TEXT,
    years_of_experience INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Courses table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'Phòng ngừa',
    level VARCHAR(50) DEFAULT 'Cơ bản', -- 'Cơ bản', 'Trung cấp', 'Nâng cao'
    is_published INTEGER NOT NULL DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- 4. Lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    video_url VARCHAR(500),
    order_index INTEGER NOT NULL DEFAULT 1,
    duration_minutes INTEGER DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- 5. Enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'enrolled', -- 'enrolled', 'in_progress', 'completed', 'dropped'
    progress_percent REAL NOT NULL DEFAULT 0.0,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE(user_id, course_id)
);

-- 6. Assessments table (Types: ASSIST, CRAFT)
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'ASSIST', 'CRAFT'
    description TEXT,
    target_group VARCHAR(100), -- 'Adults (18+)', 'Adolescents (12-21)'
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Assessment Questions
CREATE TABLE IF NOT EXISTS assessment_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 1,
    weight REAL NOT NULL DEFAULT 1.0,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
);

-- 8. Assessment Answers (Scoring options for each question)
CREATE TABLE IF NOT EXISTS assessment_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text VARCHAR(255) NOT NULL,
    score_value INTEGER NOT NULL DEFAULT 0,
    order_index INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (question_id) REFERENCES assessment_questions(id) ON DELETE CASCADE
);

-- 9. Assessment Results
CREATE TABLE IF NOT EXISTS assessment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    assessment_id INTEGER,
    total_score INTEGER NOT NULL DEFAULT 0,
    risk_level VARCHAR(50) NOT NULL, -- 'LOW', 'MODERATE', 'HIGH'
    summary TEXT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE SET NULL
);

-- 10. Recommendations (Intervention advice based on result)
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_result_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    advice_text TEXT NOT NULL,
    recommended_action VARCHAR(255),
    suggested_course_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_result_id) REFERENCES assessment_results(id) ON DELETE CASCADE,
    FOREIGN KEY (suggested_course_id) REFERENCES courses(id) ON DELETE SET NULL
);

-- 11. Working Schedules (Consultant availability)
CREATE TABLE IF NOT EXISTS working_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultant_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL, -- 0 = Thứ 2, ..., 6 = Chủ nhật
    start_time VARCHAR(10) NOT NULL, -- HH:MM format
    end_time VARCHAR(10) NOT NULL,   -- HH:MM format
    is_available INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (consultant_id) REFERENCES consultants(id) ON DELETE CASCADE
);

-- 12. Appointments (User consult appointments)
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    consultant_id INTEGER NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'confirmed', 'completed', 'cancelled'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (consultant_id) REFERENCES consultants(id) ON DELETE CASCADE
);

-- 13. Community Programs
CREATE TABLE IF NOT EXISTS community_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    max_participants INTEGER DEFAULT 100,
    status VARCHAR(50) NOT NULL DEFAULT 'upcoming', -- 'upcoming', 'ongoing', 'completed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Program Participants
CREATE TABLE IF NOT EXISTS program_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'registered', -- 'registered', 'attended', 'cancelled'
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES community_programs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(program_id, user_id)
);

-- 15. Surveys
CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 16. Survey Responses
CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER NOT NULL,
    user_id INTEGER,
    response_data TEXT NOT NULL, -- JSON formatted responses
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 17. Blog Posts
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    is_published INTEGER NOT NULL DEFAULT 1,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =========================================================================
-- SEED DATA (MANDATORY FOR TASK 2)
-- Default password for all seeded accounts is: password123
-- =========================================================================

-- 1. Seed Users (1 Admin, 2 Consultants, 3 Users)
INSERT OR IGNORE INTO users (id, username, email, password_hash, full_name, role, phone, is_active)
VALUES 
(1, 'admin', 'admin@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'Quản trị viên Hệ thống', 'ADMIN', '0901000001', 1),
(2, 'consultant1', 'consultant1@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'BS. CK1 Nguyễn Văn A', 'CONSULTANT', '0901000002', 1),
(3, 'consultant2', 'consultant2@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'ThS. Tâm lý Trần Thị B', 'CONSULTANT', '0901000003', 1),
(4, 'user1', 'user1@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'Lê Văn C', 'USER', '0901000004', 1),
(5, 'user2', 'user2@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'Phạm Thị D', 'USER', '0901000005', 1),
(6, 'user3', 'user3@community.org', 'scrypt:32768:8:1$oMIIhhM7drHTUG4c$89a7c49f25abd3f717dc02bd60853b1cecaddf146c3dabfdda5192ff2954946a5c101e30d115a16975ef65bd8ca0a158a577a24623c3fd4e0832daca4fd62b72', 'Hoàng Văn E', 'USER', '0901000006', 1);

-- 2. Seed Consultants
INSERT OR IGNORE INTO consultants (id, user_id, bio, qualifications, years_of_experience, is_active)
VALUES 
(1, 2, 'Chuyên gia tư vấn cai nghiện và phục hồi chức năng hành vi với hơn 10 năm kinh nghiệm.', 'Bác sĩ Chuyên khoa 1 Tâm thần học - Đại học Y Dược TP.HCM', 10, 1),
(2, 3, 'Chuyên viên tâm lý học vị thành niên, hỗ trợ thanh thiếu niên phòng ngừa tệ nạn và khủng hoảng tâm lý.', 'Thạc sĩ Tâm lý học Lâm sàng - Đại học Khoa học Xã hội và Nhân văn', 7, 1);

-- 3. Seed Working Schedules for Consultants
INSERT OR IGNORE INTO working_schedules (id, consultant_id, day_of_week, start_time, end_time, is_available)
VALUES 
(1, 1, 0, '08:00', '11:30', 1), -- Thứ 2 sáng
(2, 1, 2, '13:30', '17:00', 1), -- Thứ 4 chiều
(3, 1, 4, '08:00', '11:30', 1), -- Thứ 6 sáng
(4, 2, 1, '09:00', '12:00', 1), -- Thứ 3 sáng
(5, 2, 3, '14:00', '17:30', 1), -- Thứ 5 chiều
(6, 2, 5, '08:30', '11:30', 1); -- Thứ 7 sáng

-- 4. Seed Courses (At least: Nhận thức về ma túy, Kỹ năng phòng tránh, Kỹ năng từ chối, Nhận biết nguy cơ)
INSERT OR IGNORE INTO courses (id, title, description, category, level, is_published, created_by)
VALUES 
(1, 'Nhận thức về ma túy', 'Cung cấp kiến thức toàn diện về các loại ma túy phổ biến, ma túy tổng hợp mới, tác động sinh học và hủy hoại hệ thần kinh.', 'Nhận thức', 'Cơ bản', 1, 1),
(2, 'Kỹ năng phòng tránh', 'Hướng dẫn kỹ năng chủ động bảo vệ bản thân và người thân trong các môi trường có nguy cơ cao, xây dựng lối sống tích cực.', 'Kỹ năng', 'Cơ bản', 1, 1),
(3, 'Kỹ năng từ chối', 'Trang bị các chiến lược và kỹ năng giao tiếp thực tế để kiên quyết từ chối trước sự rủ rê, lôi kéo và áp lực từ bạn bè.', 'Kỹ năng', 'Trung cấp', 1, 1),
(4, 'Nhận biết nguy cơ', 'Phương pháp nhận biết các biểu hiện tâm sinh lý sớm của người có nguy cơ nghiện và các biện pháp can thiệp kịp thời.', 'Phòng ngừa', 'Trung cấp', 1, 1);

-- 5. Seed Lessons for Courses
INSERT OR IGNORE INTO lessons (id, course_id, title, content, video_url, order_index, duration_minutes)
VALUES 
(1, 1, 'Bài 1: Phân loại các nhóm chất gây nghiện hiện nay', 'Tổng quan về ma túy tự nhiên, bán tổng hợp và các loại ma túy tổng hợp thế hệ mới núp bóng đồ uống, thực phẩm.', 'https://www.youtube.com/watch?v=sample1', 1, 15),
(2, 1, 'Bài 2: Tác hại của ma túy đến não bộ và cơ thể', 'Cơ chế kích thích dopamine nhân tạo và con đường dẫn đến lệ thuộc thể chất và lệ thuộc tâm thần.', 'https://www.youtube.com/watch?v=sample2', 2, 20),
(3, 2, 'Bài 1: Xác định các môi trường tiềm ẩn rủi ro', 'Những địa điểm, tình huống xã hội dễ phát sinh việc tiếp xúc và bị lôi kéo sử dụng chất.', 'https://www.youtube.com/watch?v=sample3', 1, 15),
(4, 2, 'Bài 2: Xây dựng ranh giới cá nhân và lối sống lành mạnh', 'Các hoạt động rèn luyện thể thao, kết nối cộng đồng tích cực giúp gia tăng sức đề kháng tâm lý.', 'https://www.youtube.com/watch?v=sample4', 2, 25),
(5, 3, 'Bài 1: Kỹ thuật từ chối 3 bước', 'Bước 1: Khẳng định thái độ; Bước 2: Đưa ra lý do ngắn gọn; Bước 3: Đổi chủ đề hoặc rời khỏi vị trí nguy hiểm.', 'https://www.youtube.com/watch?v=sample5', 1, 20),
(6, 4, 'Bài 1: Các dấu hiệu thay đổi hành vi và cảm xúc', 'Cách nhận biết người thân hoặc bạn bè có dấu hiệu thay đổi bất thường về giờ giấc sinh hoạt và tài chính.', 'https://www.youtube.com/watch?v=sample6', 1, 20);

-- 6. Seed Assessments (ASSIST & CRAFT)
INSERT OR IGNORE INTO assessments (id, title, type, description, target_group, is_active)
VALUES 
(1, 'WHO ASSIST Substance Screening', 'ASSIST', 'Bộ công cụ sàng lọc sử dụng rượu, thuốc lá và các chất gây nghiện theo chuẩn WHO cho người trưởng thành (18+).', 'Adults (18+)', 1),
(2, 'CRAFFT Adolescent Substance Screening', 'CRAFT', 'Bộ câu hỏi sàng lọc hành vi nguy cơ liên quan đến chất gây nghiện cho thanh thiếu niên (12-21 tuổi).', 'Adolescents (12-21)', 1);

-- 7. Seed Assessment Questions & Answers
INSERT OR IGNORE INTO assessment_questions (id, assessment_id, question_code, question_text, order_index, weight)
VALUES 
(1, 1, 'Q1', 'Trong đời, bạn đã từng sử dụng chất gây nghiện nào chưa?', 1, 1.0),
(2, 1, 'Q2', 'Trong 3 tháng qua, tần suất bạn có cảm giác thôi thúc mạnh mẽ phải sử dụng chất là bao nhiêu?', 2, 1.0),
(3, 2, 'C', 'Bạn đã từng đi xe do một người đang say rượu hoặc dùng chất điều khiển chưa?', 1, 1.0),
(4, 2, 'R', 'Bạn có từng dùng rượu hoặc ma túy để thư giãn, cảm thấy tự tin hơn không?', 2, 1.0);

INSERT OR IGNORE INTO assessment_answers (id, question_id, answer_text, score_value, order_index)
VALUES 
(1, 1, 'Chưa bao giờ', 0, 1),
(2, 1, 'Có, nhưng rất hiếm', 2, 2),
(3, 1, 'Thường xuyên', 4, 3),
(4, 2, 'Chưa từng', 0, 1),
(5, 2, 'Hàng tháng', 3, 2),
(6, 2, 'Hàng tuần hoặc hàng ngày', 6, 3),
(7, 3, 'Không', 0, 1),
(8, 3, 'Có', 1, 2),
(9, 4, 'Không', 0, 1),
(10, 4, 'Có', 1, 2);

