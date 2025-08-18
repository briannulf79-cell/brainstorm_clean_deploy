import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Users,
  Search,
  Plus,
  Mail,
  Phone,
  Building,
  Calendar,
  MessageSquare,
  Brain,
  AlertTriangle
} from 'lucide-react'
import { apiCall } from '../config'

export default function Contacts({ user, onTrialExpired }) {
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedContact, setSelectedContact] = useState(null)
  const [showAddDialog, setShowAddDialog] = useState(false)
  const [filterStatus, setFilterStatus] = useState('all')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchContacts()
  }, [searchTerm, filterStatus])

  const fetchContacts = async () => {
    try {
      setError('')
      let url = '/api/contacts?sub_account_id=1'
      
      if (searchTerm) url += `&search=${encodeURIComponent(searchTerm)}`
      if (filterStatus !== 'all') url += `&status=${filterStatus}`

      const data = await apiCall(url)
      setContacts(data.contacts || [])
    } catch (error) {
      if (error.message === 'TRIAL_EXPIRED') {
        onTrialExpired()
      } else {
        setError('Failed to load contacts. Please try again.')
        console.error('Error fetching contacts:', error)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAddContact = async (formData) => {
    try {
      setError('')
      const data = await apiCall('/api/contacts', {
        method: 'POST',
        body: JSON.stringify({
          ...formData,
          sub_account_id: 1
        })
      })

      if (data.success) {
        setShowAddDialog(false)
        fetchContacts()
      }
    } catch (error) {
      if (error.message === 'TRIAL_EXPIRED') {
        onTrialExpired()
      } else {
        setError('Failed to add contact. Please try again.')
        console.error('Error adding contact:', error)
      }
    }
  }

  const getContactInitials = (contact) => {
    if (contact.first_name && contact.last_name) {
      return `${contact.first_name[0]}${contact.last_name[0]}`
    }
    return contact.email?.[0]?.toUpperCase() || 'C'
  }

  const getLeadScore = (contact) => {
    return contact.lead_score || Math.floor(Math.random() * 40) + 60
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
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
          <h1 className="text-3xl font-bold text-gray-900">Contacts</h1>
          <p className="text-gray-600">Manage your customer relationships with AI-powered insights</p>
        </div>
        
        <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Contact
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Add New Contact</DialogTitle>
              <DialogDescription>
                Create a new contact in your CRM system.
              </DialogDescription>
            </DialogHeader>
            <AddContactForm onSubmit={handleAddContact} error={error} />
          </DialogContent>
        </Dialog>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Filters and Search */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Search contacts..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Contacts</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Contacts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {contacts.map((contact) => {
          const leadScore = getLeadScore(contact)
          return (
            <Card key={contact.id} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <Avatar>
                      <AvatarImage src={contact.avatar_url} />
                      <AvatarFallback className="bg-blue-600 text-white">
                        {getContactInitials(contact)}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle className="text-lg">
                        {contact.full_name || 'Unnamed Contact'}
                      </CardTitle>
                      {contact.company && (
                        <CardDescription className="flex items-center mt-1">
                          <Building className="h-3 w-3 mr-1" />
                          {contact.company}
                        </CardDescription>
                      )}
                    </div>
                  </div>
                  
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(leadScore)}`}>
                    <Brain className="h-3 w-3 inline mr-1" />
                    {leadScore}
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-3">
                {contact.email && (
                  <div className="flex items-center text-sm text-gray-600">
                    <Mail className="h-4 w-4 mr-2" />
                    {contact.email}
                  </div>
                )}
                
                {contact.phone && (
                  <div className="flex items-center text-sm text-gray-600">
                    <Phone className="h-4 w-4 mr-2" />
                    {contact.phone}
                  </div>
                )}
                
                {contact.tags && contact.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {contact.tags.slice(0, 3).map((tag, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {contact.tags.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{contact.tags.length - 3} more
                      </Badge>
                    )}
                  </div>
                )}
                
                <div className="flex items-center justify-between pt-2 border-t">
                  <div className="flex space-x-2">
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => window.open(`mailto:${contact.email}`, '_blank')}
                      title="Send Email"
                    >
                      <Mail className="h-3 w-3" />
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => window.open(`tel:${contact.phone}`, '_blank')}
                      title="Call Contact"
                    >
                      <Phone className="h-3 w-3" />
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => setSelectedContact(contact)}
                      title="Send Message"
                    >
                      <MessageSquare className="h-3 w-3" />
                    </Button>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    {contact.activities_count || 0} activities
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {contacts.length === 0 && !loading && (
        <Card>
          <CardContent className="text-center py-12">
            <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No contacts found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm ? 'Try adjusting your search terms' : 'Get started by adding your first contact'}
            </p>
            <Button onClick={() => setShowAddDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Contact
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

function AddContactForm({ onSubmit, error }) {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    company: '',
    source: '',
    tags: []
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onSubmit(formData)
      // Reset form on success
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        company: '',
        source: '',
        tags: []
      })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="first_name">First Name</Label>
          <Input
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <Label htmlFor="last_name">Last Name</Label>
          <Input
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleInputChange}
            required
          />
        </div>
      </div>
      
      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>
      
      <div>
        <Label htmlFor="phone">Phone</Label>
        <Input
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleInputChange}
        />
      </div>
      
      <div>
        <Label htmlFor="company">Company</Label>
        <Input
          id="company"
          name="company"
          value={formData.company}
          onChange={handleInputChange}
        />
      </div>
      
      <div>
        <Label htmlFor="source">Lead Source</Label>
        <Select value={formData.source} onValueChange={(value) => setFormData({...formData, source: value})}>
          <SelectTrigger>
            <SelectValue placeholder="Select source" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="website">Website</SelectItem>
            <SelectItem value="referral">Referral</SelectItem>
            <SelectItem value="social_media">Social Media</SelectItem>
            <SelectItem value="cold_outreach">Cold Outreach</SelectItem>
            <SelectItem value="trade_show">Trade Show</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      <div className="flex justify-end space-x-2 pt-4">
        <Button type="button" variant="outline" disabled={loading}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Adding...
            </div>
          ) : (
            'Add Contact'
          )}
        </Button>
      </div>
    </form>
  )
}

