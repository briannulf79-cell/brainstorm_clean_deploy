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
  Users,
  DollarSign,
  TrendingUp,
  Settings,
  Globe,
  Palette,
  Code,
  Crown,
  Star,
  Building,
  Mail,
  Phone,
  Link,
  Copy,
  Check,
  Brain,
  Zap,
  Shield
} from 'lucide-react'

export default function WhiteLabelProgram() {
  const [resellers, setResellers] = useState([])
  const [selectedReseller, setSelectedReseller] = useState(null)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [copiedText, setCopiedText] = useState('')

  useEffect(() => {
    fetchResellers()
  }, [])

  const fetchResellers = async () => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockResellers = [
        {
          id: 1,
          company_name: 'Digital Marketing Pro',
          contact_name: 'John Smith',
          email: 'john@digitalmarketingpro.com',
          phone: '+1 (555) 123-4567',
          domain: 'digitalmarketingpro.com',
          subdomain: 'digitalmarketingpro.brainstormaikit.com',
          status: 'active',
          plan: 'agency',
          clients: 23,
          monthly_revenue: 6900,
          commission_rate: 30,
          total_earned: 45600,
          created_at: '2024-01-10',
          branding: {
            logo_url: null,
            primary_color: '#2563eb',
            secondary_color: '#1e40af',
            company_name: 'Digital Marketing Pro',
            support_email: 'support@digitalmarketingpro.com'
          }
        },
        {
          id: 2,
          company_name: 'Growth Solutions LLC',
          contact_name: 'Sarah Johnson',
          email: 'sarah@growthsolutions.com',
          phone: '+1 (555) 987-6543',
          domain: 'growthsolutions.com',
          subdomain: 'growthsolutions.brainstormaikit.com',
          status: 'active',
          plan: 'professional',
          clients: 12,
          monthly_revenue: 3600,
          commission_rate: 25,
          total_earned: 18900,
          created_at: '2024-01-15',
          branding: {
            logo_url: null,
            primary_color: '#059669',
            secondary_color: '#047857',
            company_name: 'Growth Solutions LLC',
            support_email: 'help@growthsolutions.com'
          }
        },
        {
          id: 3,
          company_name: 'Business Boost Agency',
          contact_name: 'Mike Wilson',
          email: 'mike@businessboost.agency',
          phone: '+1 (555) 456-7890',
          domain: null,
          subdomain: 'businessboost.brainstormaikit.com',
          status: 'pending',
          plan: 'starter',
          clients: 3,
          monthly_revenue: 900,
          commission_rate: 20,
          total_earned: 2700,
          created_at: '2024-01-20',
          branding: {
            logo_url: null,
            primary_color: '#dc2626',
            secondary_color: '#b91c1c',
            company_name: 'Business Boost Agency',
            support_email: 'support@businessboost.agency'
          }
        }
      ]
      
      setResellers(mockResellers)
    } catch (error) {
      console.error('Error fetching resellers:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'suspended': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPlanColor = (plan) => {
    switch (plan) {
      case 'agency': return 'bg-purple-100 text-purple-800'
      case 'professional': return 'bg-blue-100 text-blue-800'
      case 'starter': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const handleCopyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text)
    setCopiedText(label)
    setTimeout(() => setCopiedText(''), 2000)
  }

  const handleCreateReseller = (resellerData) => {
    const newReseller = {
      id: resellers.length + 1,
      ...resellerData,
      subdomain: `${resellerData.company_name.toLowerCase().replace(/\s+/g, '')}.brainstormaikit.com`,
      status: 'pending',
      clients: 0,
      monthly_revenue: 0,
      total_earned: 0,
      created_at: new Date().toISOString().split('T')[0],
      branding: {
        logo_url: null,
        primary_color: '#2563eb',
        secondary_color: '#1e40af',
        company_name: resellerData.company_name,
        support_email: resellerData.email
      }
    }
    
    setResellers([newReseller, ...resellers])
    setShowCreateDialog(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading white-label program...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">White-Label Reseller Program</h1>
          <p className="text-gray-600 mt-1">Empower partners to sell Brainstorm AI Kit under their own brand</p>
        </div>
        
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="h-4 w-4 mr-2" />
              Add Reseller
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Create New Reseller Account</DialogTitle>
              <DialogDescription>
                Set up a new white-label reseller partner with custom branding and commission structure.
              </DialogDescription>
            </DialogHeader>
            <CreateResellerForm onSubmit={handleCreateReseller} />
          </DialogContent>
        </Dialog>
      </div>

      {/* Program Benefits */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-l-4 border-l-blue-500">
          <CardContent className="p-6">
            <div className="flex items-center">
              <Crown className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">White-Label Branding</p>
                <p className="text-lg font-bold text-gray-900">Complete Customization</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Full branding control with custom logos, colors, and domain names
            </p>
          </CardContent>
        </Card>
        
        <Card className="border-l-4 border-l-green-500">
          <CardContent className="p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Commission Structure</p>
                <p className="text-lg font-bold text-gray-900">20-30% Revenue Share</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Competitive commission rates based on performance tiers
            </p>
          </CardContent>
        </Card>
        
        <Card className="border-l-4 border-l-purple-500">
          <CardContent className="p-6">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Full Support</p>
                <p className="text-lg font-bold text-gray-900">Training & Resources</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Complete training, marketing materials, and ongoing support
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Resellers</p>
                <p className="text-2xl font-bold text-gray-900">{resellers.filter(r => r.status === 'active').length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Building className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Clients</p>
                <p className="text-2xl font-bold text-gray-900">
                  {resellers.reduce((sum, reseller) => sum + reseller.clients, 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${resellers.reduce((sum, reseller) => sum + reseller.monthly_revenue, 0).toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Commissions</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${resellers.reduce((sum, reseller) => sum + reseller.total_earned, 0).toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Resellers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {resellers.map((reseller) => (
          <Card key={reseller.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">{reseller.company_name}</CardTitle>
                  <CardDescription className="flex items-center mt-1">
                    <Mail className="h-3 w-3 mr-1" />
                    {reseller.contact_name}
                  </CardDescription>
                </div>
                <div className="flex flex-col items-end space-y-1">
                  <Badge className={getStatusColor(reseller.status)}>
                    {reseller.status}
                  </Badge>
                  <Badge className={getPlanColor(reseller.plan)}>
                    {reseller.plan}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <p className="text-lg font-semibold text-gray-900">{reseller.clients}</p>
                  <p className="text-xs text-gray-600">Clients</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-gray-900">${reseller.monthly_revenue.toLocaleString()}</p>
                  <p className="text-xs text-gray-600">Monthly Revenue</p>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Commission Rate:</span>
                  <span className="font-medium">{reseller.commission_rate}%</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Total Earned:</span>
                  <span className="font-medium text-green-600">${reseller.total_earned.toLocaleString()}</span>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-600">Subdomain:</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleCopyToClipboard(reseller.subdomain, 'subdomain')}
                    className="h-6 px-2"
                  >
                    {copiedText === 'subdomain' ? (
                      <Check className="h-3 w-3 text-green-600" />
                    ) : (
                      <Copy className="h-3 w-3" />
                    )}
                  </Button>
                </div>
                <p className="text-xs text-blue-600 truncate">{reseller.subdomain}</p>
                
                {reseller.domain && (
                  <>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-600">Custom Domain:</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleCopyToClipboard(reseller.domain, 'domain')}
                        className="h-6 px-2"
                      >
                        {copiedText === 'domain' ? (
                          <Check className="h-3 w-3 text-green-600" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                      </Button>
                    </div>
                    <p className="text-xs text-green-600 truncate">{reseller.domain}</p>
                  </>
                )}
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  <Button size="sm" variant="outline" title="Edit Reseller">
                    <Settings className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="View Portal">
                    <Globe className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="Branding">
                    <Palette className="h-3 w-3" />
                  </Button>
                </div>
                
                <div className="text-xs text-gray-500">
                  Since {new Date(reseller.created_at).toLocaleDateString()}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {resellers.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Crown className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No resellers yet</h3>
            <p className="text-gray-600 mb-4">
              Start building your partner network with white-label reseller accounts
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Your First Reseller
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

function CreateResellerForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    company_name: '',
    contact_name: '',
    email: '',
    phone: '',
    domain: '',
    plan: 'starter',
    commission_rate: 20
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="company_name">Company Name</Label>
          <Input
            id="company_name"
            value={formData.company_name}
            onChange={(e) => setFormData({...formData, company_name: e.target.value})}
            placeholder="Digital Marketing Pro"
            required
          />
        </div>
        
        <div>
          <Label htmlFor="contact_name">Contact Name</Label>
          <Input
            id="contact_name"
            value={formData.contact_name}
            onChange={(e) => setFormData({...formData, contact_name: e.target.value})}
            placeholder="John Smith"
            required
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="email">Email Address</Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            placeholder="john@company.com"
            required
          />
        </div>
        
        <div>
          <Label htmlFor="phone">Phone Number</Label>
          <Input
            id="phone"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            placeholder="+1 (555) 123-4567"
          />
        </div>
      </div>
      
      <div>
        <Label htmlFor="domain">Custom Domain (Optional)</Label>
        <Input
          id="domain"
          value={formData.domain}
          onChange={(e) => setFormData({...formData, domain: e.target.value})}
          placeholder="www.company.com"
        />
        <p className="text-xs text-gray-500 mt-1">
          Leave empty to use subdomain: {formData.company_name.toLowerCase().replace(/\s+/g, '')}.brainstormaikit.com
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="plan">Reseller Plan</Label>
          <Select value={formData.plan} onValueChange={(value) => setFormData({...formData, plan: value})}>
            <SelectTrigger>
              <SelectValue placeholder="Select plan" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="starter">Starter (Up to 10 clients)</SelectItem>
              <SelectItem value="professional">Professional (Up to 50 clients)</SelectItem>
              <SelectItem value="agency">Agency (Unlimited clients)</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <Label htmlFor="commission_rate">Commission Rate (%)</Label>
          <Select 
            value={formData.commission_rate.toString()} 
            onValueChange={(value) => setFormData({...formData, commission_rate: parseInt(value)})}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select rate" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="20">20% (Starter)</SelectItem>
              <SelectItem value="25">25% (Professional)</SelectItem>
              <SelectItem value="30">30% (Agency)</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      
      <div className="flex justify-end space-x-2 pt-4">
        <Button 
          type="button" 
          variant="outline"
          onClick={() => window.history.back()}
        >
          Cancel
        </Button>
        <Button type="submit">
          Create Reseller Account
        </Button>
      </div>
    </form>
  )
}

