import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Brain,
  LayoutDashboard,
  Users,
  GitBranch,
  Mail,
  Zap,
  BarChart3,
  Settings,
  LogOut,
  Menu,
  X,
  Bell,
  TrendingUp,
  MessageSquare,
  Globe,
  Crown,
  Server
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Contacts', href: '/contacts', icon: Users },
  { name: 'Pipelines', href: '/pipelines', icon: GitBranch },
  { name: 'Campaigns', href: '/campaigns', icon: Mail },
  { name: 'Automation', href: '/automation', icon: Zap },
  { name: 'Funnels', href: '/funnels', icon: TrendingUp },
  { name: 'Websites', href: '/websites', icon: Globe },
  { name: 'Domains', href: '/domains', icon: Server },
  { name: 'White-Label', href: '/white-label', icon: Crown },
  { name: 'Communications', href: '/communications', icon: MessageSquare },
  { name: 'AI Insights', href: '/ai-insights', icon: Brain },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
]

export default function Layout({ children, user, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  const isActive = (href) => location.pathname === href

  const getUserInitials = (user) => {
    if (user.first_name && user.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`
    }
    return user.email[0].toUpperCase()
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
        </div>
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-slate-800 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 bg-slate-900">
          <div className="flex items-center">
            <img 
              src="/brainstorm_ai_kit_logo_icon_only.png" 
              alt="Brainstorm AI Kit" 
              className="w-8 h-8"
            />
            <span className="ml-2 text-white font-bold text-lg">Brainstorm AI Kit</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-gray-400 hover:text-white"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <nav className="mt-8 px-4">
          <div className="space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors
                    ${isActive(item.href)
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-slate-700 hover:text-white'
                    }
                  `}
                >
                  <Icon className="h-5 w-5 mr-3" />
                  {item.name}
                </Link>
              )
            })}
          </div>

          <div className="mt-8 pt-8 border-t border-slate-700">
            <Link
              to="/settings"
              onClick={() => setSidebarOpen(false)}
              className="flex items-center px-4 py-3 text-sm font-medium text-gray-300 rounded-lg hover:bg-slate-700 hover:text-white transition-colors"
            >
              <Settings className="h-5 w-5 mr-3" />
              Settings
            </Link>
          </div>
        </nav>

        {/* User info at bottom */}
        <div className="absolute bottom-0 left-0 right-0 p-4 bg-slate-900">
          <div className="flex items-center">
            <Avatar className="h-8 w-8">
              <AvatarImage src={user.avatar_url} />
              <AvatarFallback className="bg-blue-600 text-white text-sm">
                {getUserInitials(user)}
              </AvatarFallback>
            </Avatar>
            <div className="ml-3 flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">
                {user.full_name || user.email}
              </p>
              <p className="text-xs text-gray-400 truncate">
                {user.role}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top navigation */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden text-gray-500 hover:text-gray-700"
              >
                <Menu className="h-6 w-6" />
              </button>
              
              <h1 className="ml-4 lg:ml-0 text-2xl font-semibold text-gray-900">
                {navigation.find(item => isActive(item.href))?.name || 'Dashboard'}
              </h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="relative">
                    <Bell className="h-5 w-5" />
                    <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                      3
                    </span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-80" align="end">
                  <DropdownMenuLabel>Notifications</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <div className="max-h-64 overflow-y-auto">
                    <DropdownMenuItem 
                      className="flex flex-col items-start p-4 cursor-pointer hover:bg-gray-50"
                      onClick={() => window.location.href = '/pipelines'}
                    >
                      <div className="font-medium">New lead assigned</div>
                      <div className="text-sm text-gray-500">Sarah Johnson has been assigned to your pipeline</div>
                      <div className="text-xs text-gray-400 mt-1">2 minutes ago</div>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem 
                      className="flex flex-col items-start p-4 cursor-pointer hover:bg-gray-50"
                      onClick={() => window.location.href = '/campaigns'}
                    >
                      <div className="font-medium">Campaign completed</div>
                      <div className="text-sm text-gray-500">Email campaign "Summer Sale" has finished</div>
                      <div className="text-xs text-gray-400 mt-1">1 hour ago</div>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem 
                      className="flex flex-col items-start p-4 cursor-pointer hover:bg-gray-50"
                      onClick={() => window.location.href = '/ai-insights'}
                    >
                      <div className="font-medium">AI Insight available</div>
                      <div className="text-sm text-gray-500">New predictive analytics report is ready</div>
                      <div className="text-xs text-gray-400 mt-1">3 hours ago</div>
                    </DropdownMenuItem>
                  </div>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="text-center text-blue-600">
                    View all notifications
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              {/* User menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={user.avatar_url} />
                      <AvatarFallback className="bg-blue-600 text-white">
                        {getUserInitials(user)}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {user.full_name || 'User'}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <Settings className="mr-2 h-4 w-4" />
                    <span>Settings</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={onLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

