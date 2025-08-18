import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Plus,
  Eye,
  Edit,
  Copy,
  Trash2,
  BarChart3,
  Settings,
  Globe,
  Smartphone,
  Monitor,
  Zap,
  Target,
  TrendingUp,
  Users,
  MousePointer,
  DollarSign,
  Brain
} from 'lucide-react'

export default function FunnelBuilder() {
  const [funnels, setFunnels] = useState([])
  const [selectedFunnel, setSelectedFunnel] = useState(null)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFunnels()
  }, [])

  const fetchFunnels = async () => {
    try {
      // Mock data for demo
      setFunnels([
        {
          id: 1,
          name: 'Lead Generation Funnel',
          description: 'High-converting lead capture funnel with AI optimization',
          status: 'active',
          pages: [
            { id: 1, name: 'Landing Page', type: 'landing', visits: 2847, conversions: 156 },
            { id: 2, name: 'Thank You Page', type: 'thank_you', visits: 156, conversions: 89 },
            { id: 3, name: 'Upsell Page', type: 'upsell', visits: 89, conversions: 23 }
          ],
          stats: {
            total_visits: 2847,
            total_conversions: 156,
            conversion_rate: 5.48,
            revenue: 12500,
            ai_optimized: true
          },
          created_at: '2024-01-15T10:00:00Z'
        },
        {
          id: 2,
          name: 'Product Demo Funnel',
          description: 'Demo request and scheduling funnel',
          status: 'active',
          pages: [
            { id: 4, name: 'Demo Request', type: 'landing', visits: 1234, conversions: 89 },
            { id: 5, name: 'Calendar Booking', type: 'booking', visits: 89, conversions: 67 },
            { id: 6, name: 'Confirmation', type: 'confirmation', visits: 67, conversions: 67 }
          ],
          stats: {
            total_visits: 1234,
            total_conversions: 89,
            conversion_rate: 7.21,
            revenue: 8900,
            ai_optimized: false
          },
          created_at: '2024-01-12T14:30:00Z'
        },
        {
          id: 3,
          name: 'Webinar Registration',
          description: 'Webinar signup and attendance funnel',
          status: 'draft',
          pages: [
            { id: 7, name: 'Registration Page', type: 'landing', visits: 0, conversions: 0 },
            { id: 8, name: 'Thank You', type: 'thank_you', visits: 0, conversions: 0 }
          ],
          stats: {
            total_visits: 0,
            total_conversions: 0,
            conversion_rate: 0,
            revenue: 0,
            ai_optimized: false
          },
          created_at: '2024-01-10T09:15:00Z'
        }
      ])
    } catch (error) {
      console.error('Error fetching funnels:', error)
    } finally {
      setLoading(false)
    }
  }

  const createFunnel = async (funnelData) => {
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch('/api/funnels', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...funnelData,
          sub_account_id: 1
        })
      })
      
      if (response.ok) {
        const newFunnel = await response.json()
        setFunnels(prev => [...prev, newFunnel])
        setShowCreateDialog(false)
      }
    } catch (error) {
      console.error('Error creating funnel:', error)
    }
  }

  const duplicateFunnel = async (funnelId) => {
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`/api/funnels/${funnelId}/duplicate`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (response.ok) {
        const duplicatedFunnel = await response.json()
        setFunnels(prev => [...prev, duplicatedFunnel])
      }
    } catch (error) {
      console.error('Error duplicating funnel:', error)
    }
  }

  const deleteFunnel = async (funnelId) => {
    try {
      const token = localStorage.getItem('auth_token')
      await fetch(`/api/funnels/${funnelId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      setFunnels(prev => prev.filter(f => f.id !== funnelId))
    } catch (error) {
      console.error('Error deleting funnel:', error)
    }
  }

  const optimizeFunnel = async (funnelId) => {
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch(`/api/funnels/${funnelId}/ai-optimize`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (response.ok) {
        const optimizedFunnel = await response.json()
        setFunnels(prev => prev.map(f => f.id === funnelId ? optimizedFunnel : f))
      }
    } catch (error) {
      console.error('Error optimizing funnel:', error)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount)
  }

  const CreateFunnelDialog = () => {
    const [formData, setFormData] = useState({
      name: '',
      description: '',
      template: 'blank'
    })

    const templates = [
      { id: 'blank', name: 'Blank Funnel', description: 'Start from scratch' },
      { id: 'lead_gen', name: 'Lead Generation', description: 'Capture leads with opt-in form' },
      { id: 'product_demo', name: 'Product Demo', description: 'Demo request and booking' },
      { id: 'webinar', name: 'Webinar Registration', description: 'Webinar signup funnel' },
      { id: 'sales_page', name: 'Sales Page', description: 'Direct sales funnel' },
      { id: 'consultation', name: 'Consultation Booking', description: 'Book consultation calls' }
    ]

    return (
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Create New Funnel</DialogTitle>
            <DialogDescription>
              Choose a template and customize your funnel settings
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6 py-4">
            <div className="space-y-2">
              <Label htmlFor="funnel-name">Funnel Name</Label>
              <Input
                id="funnel-name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter funnel name"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="funnel-description">Description</Label>
              <Textarea
                id="funnel-description"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Describe your funnel purpose"
                rows={3}
              />
            </div>
            
            <div className="space-y-3">
              <Label>Choose Template</Label>
              <div className="grid grid-cols-2 gap-3">
                {templates.map((template) => (
                  <Card 
                    key={template.id}
                    className={`cursor-pointer transition-all ${
                      formData.template === template.id 
                        ? 'ring-2 ring-blue-500 bg-blue-50' 
                        : 'hover:shadow-md'
                    }`}
                    onClick={() => setFormData(prev => ({ ...prev, template: template.id }))}
                  >
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">{template.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <p className="text-xs text-gray-600">{template.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
              Cancel
            </Button>
            <Button onClick={() => createFunnel(formData)} disabled={!formData.name}>
              Create Funnel
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Funnel Builder</h1>
          <p className="text-gray-600">Create high-converting sales funnels with AI optimization</p>
        </div>
        
        <Button onClick={() => setShowCreateDialog(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Create Funnel
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Funnels</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{funnels.length}</div>
            <p className="text-xs text-muted-foreground">
              {funnels.filter(f => f.status === 'active').length} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Visits</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {funnels.reduce((sum, f) => sum + f.stats.total_visits, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              This month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversions</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {funnels.reduce((sum, f) => sum + f.stats.total_conversions, 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {((funnels.reduce((sum, f) => sum + f.stats.total_conversions, 0) / 
                 funnels.reduce((sum, f) => sum + f.stats.total_visits, 0)) * 100).toFixed(1)}% avg rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(funnels.reduce((sum, f) => sum + f.stats.revenue, 0))}
            </div>
            <p className="text-xs text-muted-foreground">
              From all funnels
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Funnels Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {funnels.map((funnel) => (
          <Card key={funnel.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <CardTitle className="text-lg">{funnel.name}</CardTitle>
                    {funnel.stats.ai_optimized && (
                      <Brain className="h-4 w-4 text-blue-600" />
                    )}
                  </div>
                  <CardDescription>{funnel.description}</CardDescription>
                </div>
                <Badge className={getStatusColor(funnel.status)}>
                  {funnel.status}
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Performance Metrics */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <div className="text-gray-500">Visits</div>
                  <div className="font-semibold">{funnel.stats.total_visits.toLocaleString()}</div>
                </div>
                <div>
                  <div className="text-gray-500">Conversions</div>
                  <div className="font-semibold">{funnel.stats.total_conversions}</div>
                </div>
                <div>
                  <div className="text-gray-500">Conv. Rate</div>
                  <div className="font-semibold text-green-600">
                    {funnel.stats.conversion_rate.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">Revenue</div>
                  <div className="font-semibold">{formatCurrency(funnel.stats.revenue)}</div>
                </div>
              </div>

              {/* Pages */}
              <div>
                <div className="text-sm font-medium mb-2">Pages ({funnel.pages.length})</div>
                <div className="space-y-1">
                  {funnel.pages.slice(0, 3).map((page) => (
                    <div key={page.id} className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">{page.name}</span>
                      <span className="font-medium">
                        {page.conversions}/{page.visits}
                      </span>
                    </div>
                  ))}
                  {funnel.pages.length > 3 && (
                    <div className="text-xs text-gray-500">
                      +{funnel.pages.length - 3} more pages
                    </div>
                  )}
                </div>
              </div>

              {/* AI Optimization */}
              {!funnel.stats.ai_optimized && funnel.stats.total_visits > 100 && (
                <div className="p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center mb-1">
                    <Brain className="h-4 w-4 text-blue-600 mr-2" />
                    <span className="text-sm font-medium text-blue-800">AI Optimization Available</span>
                  </div>
                  <p className="text-xs text-blue-700 mb-2">
                    Improve conversion rates with AI-powered optimization
                  </p>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="w-full"
                    onClick={() => optimizeFunnel(funnel.id)}
                  >
                    <Zap className="h-3 w-3 mr-1" />
                    Optimize
                  </Button>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  <Button size="sm" variant="outline">
                    <Eye className="h-3 w-3 mr-1" />
                    View
                  </Button>
                  <Button size="sm" variant="outline">
                    <Edit className="h-3 w-3 mr-1" />
                    Edit
                  </Button>
                  <Button size="sm" variant="outline">
                    <BarChart3 className="h-3 w-3 mr-1" />
                    Stats
                  </Button>
                </div>
                
                <div className="flex space-x-1">
                  <Button 
                    size="sm" 
                    variant="ghost"
                    onClick={() => duplicateFunnel(funnel.id)}
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                  <Button 
                    size="sm" 
                    variant="ghost"
                    onClick={() => deleteFunnel(funnel.id)}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {funnels.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No funnels yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first funnel to start converting visitors into customers
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Funnel
            </Button>
          </CardContent>
        </Card>
      )}

      <CreateFunnelDialog />
    </div>
  )
}

