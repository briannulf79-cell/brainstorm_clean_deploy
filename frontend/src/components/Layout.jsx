import { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Avatar, AvatarFallback } from './ui/avatar';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from './ui/dropdown-menu';
import { Badge } from './ui/badge';
import {
  Brain,
  Lightbulb,
  LayoutDashboard,
  Users,
  GitBranch,
  MessageSquare,
  BarChart3,
  Settings,
  Bell,
  LogOut,
  Menu,
  X,
  Globe,
  FileText,
  ShoppingCart,
  Building,
  Zap,
  Crown
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Contacts', href: '/dashboard/contacts', icon: Users },
  { name: 'Websites', href: '/dashboard/websites', icon: Globe, master: false },
  { name: 'Content', href: '/dashboard/content', icon: FileText, master: false },
  { name: 'Funnels', href: '/dashboard/funnels', icon: GitBranch, master: false },
  { name: 'E-commerce', href: '/dashboard/ecommerce', icon: ShoppingCart, master: false },
  { name: 'Sub-Accounts', href: '/dashboard/sub-accounts', icon: Building, master: true },
  { name: 'Automation', href: '/dashboard/automation', icon: Zap, master: false },
  { name: 'Messages', href: '/dashboard/messages', icon: MessageSquare },
  { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const userInitials = user.name ? user.name.split(' ').map(n => n[0]).join('').toUpperCase() : 'U';

  const handleLogout = async () => {
    try {
      // Call logout endpoint
      await fetch(`${import.meta.env.VITE_API_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/');
    }
  };

  const isMasterAccount = user.role === 'master';
  const isTrialUser = !isMasterAccount && user.subscription_status === 'trial';
  const trialDaysLeft = user.days_remaining || 30;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0`}>
        <div className="flex items-center justify-between h-16 px-6 border-b">
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Brain className="h-8 w-8 text-blue-600" />
              <Lightbulb className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1" />
            </div>
            <span className="text-xl font-bold text-gray-900">Brainstorm AI</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Account Status Banner */}
        {isMasterAccount ? (
          <div className="mx-4 mt-4 p-3 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-900 flex items-center">
                  <Crown className="w-4 h-4 mr-1 text-yellow-600" />
                  Master Account
                </p>
                <p className="text-xs text-green-700">Unlimited Access</p>
              </div>
              <Button size="sm" className="text-xs bg-blue-600 hover:bg-blue-700">
                Manage
              </Button>
            </div>
          </div>
        ) : isTrialUser && (
          <div className="mx-4 mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-900">Free Trial</p>
                <p className="text-xs text-blue-700">{trialDaysLeft} days left</p>
              </div>
              <Button size="sm" className="text-xs">
                Upgrade
              </Button>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="mt-6 px-4">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const showItem = !item.master || (item.master && isMasterAccount);
              
              if (!showItem) return null;
              
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.name}
                    {item.master && (
                      <Crown className="ml-auto h-3 w-3 text-yellow-600" />
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-40 bg-white shadow-sm border-b">
          <div className="flex items-center justify-between h-16 px-4 sm:px-6">
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="relative">
                    <Bell className="h-5 w-5" />
                    <Badge 
                      variant="destructive" 
                      className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center text-xs"
                    >
                      3
                    </Badge>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-80">
                  <div className="p-4">
                    <h3 className="font-semibold text-sm">Notifications</h3>
                    <div className="mt-2 space-y-2">
                      <div className="p-2 bg-blue-50 rounded text-sm">
                        <p className="font-medium">New contact added</p>
                        <p className="text-gray-600">Sarah Johnson joined your pipeline</p>
                      </div>
                      <div className="p-2 bg-green-50 rounded text-sm">
                        <p className="font-medium">Deal closed</p>
                        <p className="text-gray-600">$5,000 deal with TechCorp completed</p>
                      </div>
                      <div className="p-2 bg-yellow-50 rounded text-sm">
                        <p className="font-medium">Trial reminder</p>
                        <p className="text-gray-600">Your trial expires in {trialDaysLeft} days</p>
                      </div>
                    </div>
                  </div>
                </DropdownMenuContent>
              </DropdownMenu>

              {/* User menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback>{userInitials}</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <div className="px-2 py-1.5">
                    <p className="text-sm font-medium">{user.name || 'User'}</p>
                    <p className="text-xs text-gray-500">{user.email}</p>
                  </div>
                  <DropdownMenuItem>
                    <Settings className="mr-2 h-4 w-4" />
                    Settings
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

