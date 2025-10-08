import { Heart, Activity, Utensils, TrendingUp } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Heart className="h-8 w-8 text-primary-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">Health Tracker</h1>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-500 hover:text-gray-900">Trang chủ</a>
              <a href="#" className="text-gray-500 hover:text-gray-900">Nhật ký ăn uống</a>
              <a href="#" className="text-gray-500 hover:text-gray-900">Tập luyện</a>
              <a href="#" className="text-gray-500 hover:text-gray-900">Phân tích</a>
            </nav>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              Đăng nhập
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Theo dõi sức khỏe và dinh dưỡng thông minh
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Ứng dụng AI giúp bạn quản lý dinh dưỡng, theo dõi calo và đưa ra gợi ý 
            cá nhân hóa cho sức khỏe tốt hơn với cơ sở dữ liệu món ăn Việt Nam.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700">
              Bắt đầu ngay
            </button>
            <button className="border border-primary-600 text-primary-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-50">
              Tìm hiểu thêm
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Tính năng chính
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Utensils className="h-8 w-8 text-primary-600" />
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Nhật ký ăn uống</h4>
              <p className="text-gray-600">Ghi chép và theo dõi các bữa ăn hàng ngày</p>
            </div>
            <div className="text-center">
              <div className="bg-health-green/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Activity className="h-8 w-8 text-health-green" />
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Tập luyện</h4>
              <p className="text-gray-600">Theo dõi hoạt động thể chất và đốt cháy calo</p>
            </div>
            <div className="text-center">
              <div className="bg-health-orange/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-8 w-8 text-health-orange" />
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Phân tích AI</h4>
              <p className="text-gray-600">Gợi ý thông minh dựa trên dữ liệu cá nhân</p>
            </div>
            <div className="text-center">
              <div className="bg-health-red/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-health-red" />
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Sức khỏe</h4>
              <p className="text-gray-600">Theo dõi tiến độ và mục tiêu sức khỏe</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <Heart className="h-6 w-6 text-primary-400" />
              <span className="ml-2 text-xl font-bold">Health Tracker</span>
            </div>
            <p className="text-gray-400">
              © 2024 Health Tracker. Dự án tốt nghiệp - Ứng dụng theo dõi sức khỏe và dinh dưỡng với AI.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
