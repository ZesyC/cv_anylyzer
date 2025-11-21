import { TranslationKeys } from './en';

export const vi: TranslationKeys = {
  // Header
  header: {
    title: "Phân Tích CV",
    subtitle: "Nhận gợi ý từ AI để cải thiện CV và nổi bật với nhà tuyển dụng"
  },

  // File Upload Form
  upload: {
    title: "Tải Lên CV Của Bạn",
    dragDrop: "Kéo và thả CV của bạn vào đây, hoặc",
    browse: "Chọn Tệp",
    supportedFormats: "Hỗ trợ PDF và DOCX (tối đa 10 MB)",
    fileName: "Đã chọn tệp",
    chooseAnother: "Chọn tệp khác",
    jdLabel: "Mô Tả Công Việc (Tùy chọn)",
    jdPlaceholder: "Dán mô tả công việc vào đây để nhận gợi ý phù hợp...",
    analyzeButton: "Phân Tích CV",
    analyzing: "Đang phân tích..."
  },

  // Analysis Result
  analysis: {
    title: "Kết Quả Phân Tích",
    overallSummary: "Tổng Quan",
    strengths: "Điểm Mạnh",
    weaknesses: "Điểm Cần Cải Thiện",
    detailedSuggestions: "Gợi Ý Chi Tiết",
    backToTop: "↑ Về Đầu Trang",
    analyzeAnother: "← Phân Tích CV Khác"
  },

  // Section Checklist
  sections: {
    title: "📋 Danh Sách Các Phần",
    professionalSummary: "Tóm Tắt Chuyên Môn",
    skills: "Kỹ Năng",
    experience: "Kinh Nghiệm",
    projects: "Dự Án",
    education: "Học Vấn",
    present: "Có",
    missing: "Thiếu"
  },

  // Keyword Match
  keywords: {
    title: "🎯 Phân Tích Từ Khóa",
    matched: "Từ Khóa Khớp",
    missing: "Từ Khóa Thiếu",
    noMatched: "Không tìm thấy từ khóa khớp",
    allPresent: "Tất cả từ khóa trong JD đều có trong CV của bạn!",
    tip: "💡 Mẹo:",
    tipText: "Hãy cân nhắc bổ sung các từ khóa còn thiếu vào CV của bạn để phù hợp hơn với mô tả công việc."
  },

  // Suggestions
  suggestions: {
    issuesFound: "Vấn Đề Phát Hiện:",
    suggestions: "Gợi Ý:",
    exampleImprovements: "Ví Dụ Cải Thiện:",
    example: "Ví dụ",
    original: "Ban đầu:",
    improved: "Cải thiện:"
  },

  // Error States
  error: {
    title: "Phân Tích Thất Bại"
  },

  // Loading States
  loading: {
    title: "Đang Phân Tích CV...",
    subtitle: "Đang trích xuất văn bản, phát hiện các phần và tạo phản hồi cá nhân hóa"
  },

  // Empty State
  empty: {
    title: "Sẵn sàng cải thiện CV?",
    subtitle: "Tải lên CV của bạn ở trên để bắt đầu phân tích và nhận gợi ý từ AI"
  },

  // Footer
  footer: {
    builtWith: "Được xây dựng với Zéy"
  }
};
