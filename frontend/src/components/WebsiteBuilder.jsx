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
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import {
  Plus,
  Eye,
  Edit,
  Copy,
  Trash2,
  Settings,
  Globe,
  Smartphone,
  Monitor,
  Code,
  Palette,
  Layout,
  Image,
  Type,
  MousePointer,
  Zap,
  Brain,
  ShoppingCart,
  Calendar,
  Mail,
  Phone
} from 'lucide-react'

export default function WebsiteBuilder() {
  const [websites, setWebsites] = useState([])
  const [selectedWebsite, setSelectedWebsite] = useState(null)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchWebsites()
  }, [])

  const fetchWebsites = async () => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockWebsites = [
        {
          id: 1,
          name: 'Business Landing Page',
          domain: 'mybusiness.brainstormaikit.com',
          custom_domain: 'www.mybusiness.com',
          template: 'Business Pro',
          status: 'published',
          visits: 1247,
          conversions: 23,
          conversion_rate: 1.8,
          created_at: '2024-01-15',
          last_updated: '2024-01-20',
          pages: 5,
          ssl_enabled: true,
          mobile_optimized: true
        },
        {
          id: 2,
          name: 'E-commerce Store',
          domain: 'store.brainstormaikit.com',
          custom_domain: null,
          template: 'E-commerce Plus',
          status: 'draft',
          visits: 0,
          conversions: 0,
          conversion_rate: 0,
          created_at: '2024-01-18',
          last_updated: '2024-01-18',
          pages: 8,
          ssl_enabled: true,
          mobile_optimized: true
        },
        {
          id: 3,
          name: 'Portfolio Website',
          domain: 'portfolio.brainstormaikit.com',
          custom_domain: 'www.johnsmith.design',
          template: 'Creative Portfolio',
          status: 'published',
          visits: 892,
          conversions: 12,
          conversion_rate: 1.3,
          created_at: '2024-01-10',
          last_updated: '2024-01-19',
          pages: 6,
          ssl_enabled: true,
          mobile_optimized: true
        }
      ]
      
      setWebsites(mockWebsites)
    } catch (error) {
      console.error('Error fetching websites:', error)
    } finally {
      setLoading(false)
    }
  }

  const templates = [
    {
      id: 'business-pro',
      name: 'Business Pro',
      description: 'Professional business website with contact forms and service pages',
      category: 'Business',
      preview: '/api/placeholder/300/200',
      features: ['Contact Forms', 'Service Pages', 'Testimonials', 'Blog']
    },
    {
      id: 'ecommerce-plus',
      name: 'E-commerce Plus',
      description: 'Complete online store with shopping cart and payment integration',
      category: 'E-commerce',
      preview: '/api/placeholder/300/200',
      features: ['Shopping Cart', 'Payment Gateway', 'Product Catalog', 'Inventory Management']
    },
    {
      id: 'creative-portfolio',
      name: 'Creative Portfolio',
      description: 'Stunning portfolio website for creatives and professionals',
      category: 'Portfolio',
      preview: '/api/placeholder/300/200',
      features: ['Gallery', 'Project Showcase', 'Contact Form', 'Blog']
    },
    {
      id: 'restaurant-menu',
      name: 'Restaurant & Menu',
      description: 'Beautiful restaurant website with online menu and reservations',
      category: 'Restaurant',
      preview: '/api/placeholder/300/200',
      features: ['Online Menu', 'Reservations', 'Gallery', 'Contact Info']
    },
    {
      id: 'fitness-gym',
      name: 'Fitness & Gym',
      description: 'Dynamic fitness website with class schedules and membership signup',
      category: 'Fitness',
      preview: '/api/placeholder/300/200',
      features: ['Class Schedules', 'Membership Signup', 'Trainer Profiles', 'Blog']
    },
    {
      id: 'real-estate',
      name: 'Real Estate',
      description: 'Professional real estate website with property listings',
      category: 'Real Estate',
      preview: '/api/placeholder/300/200',
      features: ['Property Listings', 'Search Filters', 'Agent Profiles', 'Contact Forms']
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800'
      case 'draft': return 'bg-yellow-100 text-yellow-800'
      case 'archived': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const handleCreateWebsite = (websiteData) => {
    const newWebsite = {
      id: websites.length + 1,
      ...websiteData,
      domain: `${websiteData.name.toLowerCase().replace(/\s+/g, '-')}.brainstormaikit.com`,
      status: 'draft',
      visits: 0,
      conversions: 0,
      conversion_rate: 0,
      created_at: new Date().toISOString().split('T')[0],
      last_updated: new Date().toISOString().split('T')[0],
      pages: 1,
      ssl_enabled: true,
      mobile_optimized: true
    }
    
    setWebsites([newWebsite, ...websites])
    setShowCreateDialog(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading websites...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Website Builder</h1>
          <p className="text-gray-600 mt-1">Create unlimited professional websites with AI-powered optimization</p>
        </div>
        
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="h-4 w-4 mr-2" />
              Create Website
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Create New Website</DialogTitle>
              <DialogDescription>
                Choose a template and customize your website. All websites include free SSL, mobile optimization, and AI-powered features.
              </DialogDescription>
            </DialogHeader>
            
            <Tabs defaultValue="templates" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="templates">Choose Template</TabsTrigger>
                <TabsTrigger value="details">Website Details</TabsTrigger>
              </TabsList>
              
              <TabsContent value="templates" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {templates.map((template) => (
                    <Card key={template.id} className="cursor-pointer hover:shadow-lg transition-shadow">
                      <CardHeader className="p-0">
                        <div className="h-40 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-t-lg flex items-center justify-center">
                          <Layout className="h-16 w-16 text-blue-600" />
                        </div>
                      </CardHeader>
                      <CardContent className="p-4">
                        <CardTitle className="text-lg mb-2">{template.name}</CardTitle>
                        <CardDescription className="text-sm mb-3">
                          {template.description}
                        </CardDescription>
                        <div className="flex flex-wrap gap-1 mb-3">
                          {template.features.slice(0, 2).map((feature, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {feature}
                            </Badge>
                          ))}
                          {template.features.length > 2 && (
                            <Badge variant="outline" className="text-xs">
                              +{template.features.length - 2} more
                            </Badge>
                          )}
                        </div>
                        <Button className="w-full" size="sm">
                          Select Template
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="details" className="space-y-4">
                <CreateWebsiteForm onSubmit={handleCreateWebsite} />
              </TabsContent>
            </Tabs>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Globe className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Websites</p>
                <p className="text-2xl font-bold text-gray-900">{websites.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Eye className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Visits</p>
                <p className="text-2xl font-bold text-gray-900">
                  {websites.reduce((sum, site) => sum + site.visits, 0).toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <MousePointer className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Conversions</p>
                <p className="text-2xl font-bold text-gray-900">
                  {websites.reduce((sum, site) => sum + site.conversions, 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">AI Optimizations</p>
                <p className="text-2xl font-bold text-gray-900">47</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Websites Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {websites.map((website) => (
          <Card key={website.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">{website.name}</CardTitle>
                  <CardDescription className="flex items-center mt-1">
                    <Globe className="h-3 w-3 mr-1" />
                    {website.custom_domain || website.domain}
                  </CardDescription>
                </div>
                <Badge className={getStatusColor(website.status)}>
                  {website.status}
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="h-32 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg flex items-center justify-center">
                <Monitor className="h-12 w-12 text-gray-400" />
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-lg font-semibold text-gray-900">{website.visits.toLocaleString()}</p>
                  <p className="text-xs text-gray-600">Visits</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-gray-900">{website.conversions}</p>
                  <p className="text-xs text-gray-600">Conversions</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-gray-900">{website.conversion_rate}%</p>
                  <p className="text-xs text-gray-600">Conv. Rate</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  <Button size="sm" variant="outline" title="Preview Website">
                    <Eye className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="Edit Website">
                    <Edit className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="Website Settings">
                    <Settings className="h-3 w-3" />
                  </Button>
                </div>
                
                <div className="text-xs text-gray-500">
                  {website.pages} pages
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {websites.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Globe className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No websites yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first website with our AI-powered builder and professional templates
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Website
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

function CreateWebsiteForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    template: '',
    description: '',
    industry: '',
    custom_domain: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="name">Website Name</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            placeholder="My Business Website"
            required
          />
        </div>
        
        <div>
          <Label htmlFor="industry">Industry</Label>
          <Select value={formData.industry} onValueChange={(value) => setFormData({...formData, industry: value})}>
            <SelectTrigger>
              <SelectValue placeholder="Select industry" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="business">Business Services</SelectItem>
              <SelectItem value="ecommerce">E-commerce</SelectItem>
              <SelectItem value="restaurant">Restaurant</SelectItem>
              <SelectItem value="fitness">Fitness & Health</SelectItem>
              <SelectItem value="realestate">Real Estate</SelectItem>
              <SelectItem value="creative">Creative & Portfolio</SelectItem>
              <SelectItem value="nonprofit">Non-Profit</SelectItem>
              <SelectItem value="education">Education</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      
      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          placeholder="Brief description of your website purpose..."
          rows={3}
        />
      </div>
      
      <div>
        <Label htmlFor="custom_domain">Custom Domain (Optional)</Label>
        <Input
          id="custom_domain"
          value={formData.custom_domain}
          onChange={(e) => setFormData({...formData, custom_domain: e.target.value})}
          placeholder="www.yourdomain.com"
        />
        <p className="text-xs text-gray-500 mt-1">
          Leave empty to use free subdomain: {formData.name.toLowerCase().replace(/\s+/g, '-')}.brainstormaikit.com
        </p>
      </div>
      
      <div className="flex justify-end space-x-2 pt-4">
        <Button type="button" variant="outline">
          Cancel
        </Button>
        <Button type="submit">
          Create Website
        </Button>
      </div>
    </form>
  )
}

