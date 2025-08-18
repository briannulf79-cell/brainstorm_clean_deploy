import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
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
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import {
  Plus,
  Search,
  Globe,
  Shield,
  Settings,
  RotateCcw,
  ExternalLink,
  CheckCircle,
  AlertCircle,
  Clock,
  DollarSign,
  Calendar,
  Zap,
  Lock,
  Unlock,
  Copy,
  Check,
  CreditCard,
  Server,
  Mail
} from 'lucide-react'

export default function DomainManager() {
  const [domains, setDomains] = useState([])
  const [searchResults, setSearchResults] = useState([])
  const [selectedDomain, setSelectedDomain] = useState(null)
  const [showSearchDialog, setShowSearchDialog] = useState(false)
  const [showPurchaseDialog, setShowPurchaseDialog] = useState(false)
  const [loading, setLoading] = useState(true)
  const [searching, setSearching] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [copiedText, setCopiedText] = useState('')

  useEffect(() => {
    fetchDomains()
  }, [])

  const fetchDomains = async () => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockDomains = [
        {
          id: 1,
          domain: 'mybusiness.com',
          status: 'active',
          expires_at: '2025-01-15',
          auto_renew: true,
          privacy_protection: true,
          ssl_enabled: true,
          dns_managed: true,
          registrar: 'Brainstorm AI Kit',
          price_paid: 12.99,
          renewal_price: 14.99,
          created_at: '2024-01-15',
          connected_services: ['Website', 'Email'],
          nameservers: [
            'ns1.brainstormaikit.com',
            'ns2.brainstormaikit.com'
          ]
        },
        {
          id: 2,
          domain: 'growthagency.net',
          status: 'pending_transfer',
          expires_at: '2024-12-20',
          auto_renew: false,
          privacy_protection: false,
          ssl_enabled: false,
          dns_managed: false,
          registrar: 'External',
          price_paid: 0,
          renewal_price: 16.99,
          created_at: '2024-01-20',
          connected_services: [],
          nameservers: [
            'ns1.externalprovider.com',
            'ns2.externalprovider.com'
          ]
        },
        {
          id: 3,
          domain: 'digitalmarketing.pro',
          status: 'expired',
          expires_at: '2024-01-10',
          auto_renew: false,
          privacy_protection: true,
          ssl_enabled: false,
          dns_managed: true,
          registrar: 'Brainstorm AI Kit',
          price_paid: 24.99,
          renewal_price: 29.99,
          created_at: '2023-01-10',
          connected_services: ['Website'],
          nameservers: [
            'ns1.brainstormaikit.com',
            'ns2.brainstormaikit.com'
          ]
        }
      ]
      
      setDomains(mockDomains)
    } catch (error) {
      console.error('Error fetching domains:', error)
    } finally {
      setLoading(false)
    }
  }

  const searchDomains = async (term) => {
    setSearching(true)
    try {
      // Simulate domain search API
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const extensions = ['.com', '.net', '.org', '.io', '.co', '.ai', '.app', '.dev']
      const mockResults = extensions.map(ext => ({
        domain: `${term}${ext}`,
        available: Math.random() > 0.4,
        price: Math.floor(Math.random() * 30) + 10,
        premium: Math.random() > 0.8,
        popular: ext === '.com' || ext === '.net'
      }))
      
      setSearchResults(mockResults)
    } catch (error) {
      console.error('Error searching domains:', error)
    } finally {
      setSearching(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'pending_transfer': return 'bg-yellow-100 text-yellow-800'
      case 'expired': return 'bg-red-100 text-red-800'
      case 'suspended': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'pending_transfer': return <Clock className="h-4 w-4 text-yellow-600" />
      case 'expired': return <AlertCircle className="h-4 w-4 text-red-600" />
      default: return <AlertCircle className="h-4 w-4 text-gray-600" />
    }
  }

  const handleCopyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text)
    setCopiedText(label)
    setTimeout(() => setCopiedText(''), 2000)
  }

  const handlePurchaseDomain = (domainData) => {
    const newDomain = {
      id: domains.length + 1,
      domain: domainData.domain,
      status: 'active',
      expires_at: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      auto_renew: true,
      privacy_protection: true,
      ssl_enabled: true,
      dns_managed: true,
      registrar: 'Brainstorm AI Kit',
      price_paid: domainData.price,
      renewal_price: domainData.price,
      created_at: new Date().toISOString().split('T')[0],
      connected_services: [],
      nameservers: [
        'ns1.brainstormaikit.com',
        'ns2.brainstormaikit.com'
      ]
    }
    
    setDomains([newDomain, ...domains])
    setShowPurchaseDialog(false)
    setSelectedDomain(null)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading domains...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Domain Manager</h1>
          <p className="text-gray-600 mt-1">Purchase, manage, and configure domains for your websites and services</p>
        </div>
        
        <Dialog open={showSearchDialog} onOpenChange={setShowSearchDialog}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="h-4 w-4 mr-2" />
              Search Domains
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Search & Purchase Domains</DialogTitle>
              <DialogDescription>
                Find the perfect domain for your website. All domains include free DNS management, SSL certificates, and privacy protection.
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4">
              <div className="flex space-x-2">
                <Input
                  placeholder="Enter domain name (without extension)"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && searchTerm && searchDomains(searchTerm)}
                />
                <Button 
                  onClick={() => searchTerm && searchDomains(searchTerm)}
                  disabled={searching || !searchTerm}
                >
                  {searching ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  ) : (
                    <Search className="h-4 w-4" />
                  )}
                </Button>
              </div>
              
              {searching && (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Searching available domains...</p>
                </div>
              )}
              
              {searchResults.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {searchResults.map((result, index) => (
                    <Card key={index} className={`${result.available ? 'border-green-200' : 'border-gray-200'}`}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-medium text-lg">{result.domain}</p>
                            <div className="flex items-center space-x-2 mt-1">
                              {result.available ? (
                                <Badge className="bg-green-100 text-green-800">Available</Badge>
                              ) : (
                                <Badge className="bg-red-100 text-red-800">Taken</Badge>
                              )}
                              {result.premium && (
                                <Badge className="bg-purple-100 text-purple-800">Premium</Badge>
                              )}
                              {result.popular && (
                                <Badge className="bg-blue-100 text-blue-800">Popular</Badge>
                              )}
                            </div>
                          </div>
                          
                          <div className="text-right">
                            <p className="text-2xl font-bold text-gray-900">${result.price}</p>
                            <p className="text-xs text-gray-600">/year</p>
                            {result.available && (
                              <Button 
                                size="sm" 
                                className="mt-2"
                                onClick={() => {
                                  setSelectedDomain(result)
                                  setShowPurchaseDialog(true)
                                }}
                              >
                                Purchase
                              </Button>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
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
                <p className="text-sm font-medium text-gray-600">Total Domains</p>
                <p className="text-2xl font-bold text-gray-900">{domains.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Domains</p>
                <p className="text-2xl font-bold text-gray-900">
                  {domains.filter(d => d.status === 'active').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Calendar className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Expiring Soon</p>
                <p className="text-2xl font-bold text-gray-900">
                  {domains.filter(d => {
                    const expiry = new Date(d.expires_at)
                    const now = new Date()
                    const diffDays = (expiry - now) / (1000 * 60 * 60 * 24)
                    return diffDays <= 30 && diffDays > 0
                  }).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">SSL Protected</p>
                <p className="text-2xl font-bold text-gray-900">
                  {domains.filter(d => d.ssl_enabled).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Domains Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {domains.map((domain) => (
          <Card key={domain.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg flex items-center">
                    {getStatusIcon(domain.status)}
                    <span className="ml-2">{domain.domain}</span>
                  </CardTitle>
                  <CardDescription className="flex items-center mt-1">
                    <Calendar className="h-3 w-3 mr-1" />
                    Expires {new Date(domain.expires_at).toLocaleDateString()}
                  </CardDescription>
                </div>
                <Badge className={getStatusColor(domain.status)}>
                  {domain.status.replace('_', ' ')}
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center space-x-2">
                  {domain.ssl_enabled ? (
                    <Lock className="h-4 w-4 text-green-600" />
                  ) : (
                    <Unlock className="h-4 w-4 text-red-600" />
                  )}
                  <span className="text-sm text-gray-600">SSL</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  {domain.privacy_protection ? (
                    <Shield className="h-4 w-4 text-green-600" />
                  ) : (
                    <Shield className="h-4 w-4 text-red-600" />
                  )}
                  <span className="text-sm text-gray-600">Privacy</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  {domain.auto_renew ? (
                    <RotateCcw className="h-4 w-4 text-green-600" />
                  ) : (
                    <RotateCcw className="h-4 w-4 text-red-600" />
                  )}
                  <span className="text-sm text-gray-600">Auto-Renew</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  {domain.dns_managed ? (
                    <Server className="h-4 w-4 text-green-600" />
                  ) : (
                    <Server className="h-4 w-4 text-red-600" />
                  )}
                  <span className="text-sm text-gray-600">DNS</span>
                </div>
              </div>
              
              {domain.connected_services.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Connected Services:</p>
                  <div className="flex flex-wrap gap-1">
                    {domain.connected_services.map((service, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {service}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Renewal Price:</span>
                  <span className="font-medium">${domain.renewal_price}/year</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Registrar:</span>
                  <span className="font-medium">{domain.registrar}</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  <Button size="sm" variant="outline" title="Domain Settings">
                    <Settings className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="DNS Management">
                    <Server className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" title="SSL Certificate">
                    <Shield className="h-3 w-3" />
                  </Button>
                </div>
                
                <div className="text-xs text-gray-500">
                  {Math.ceil((new Date(domain.expires_at) - new Date()) / (1000 * 60 * 60 * 24))} days left
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {domains.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Globe className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No domains yet</h3>
            <p className="text-gray-600 mb-4">
              Search and purchase domains to get started with your online presence
            </p>
            <Button onClick={() => setShowSearchDialog(true)}>
              <Search className="h-4 w-4 mr-2" />
              Search Your First Domain
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Purchase Dialog */}
      <Dialog open={showPurchaseDialog} onOpenChange={setShowPurchaseDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Purchase Domain</DialogTitle>
            <DialogDescription>
              Complete your domain purchase with included features
            </DialogDescription>
          </DialogHeader>
          
          {selectedDomain && (
            <div className="space-y-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-lg">{selectedDomain.domain}</p>
                      <p className="text-sm text-gray-600">1 year registration</p>
                    </div>
                    <p className="text-2xl font-bold">${selectedDomain.price}</p>
                  </div>
                </CardContent>
              </Card>
              
              <div className="space-y-2">
                <h4 className="font-medium">Included Features:</h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span>Free DNS Management</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span>Free SSL Certificate</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span>Privacy Protection</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span>Email Forwarding</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowPurchaseDialog(false)}>
              Cancel
            </Button>
            <Button onClick={() => selectedDomain && handlePurchaseDomain(selectedDomain)}>
              <CreditCard className="h-4 w-4 mr-2" />
              Purchase Domain
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

