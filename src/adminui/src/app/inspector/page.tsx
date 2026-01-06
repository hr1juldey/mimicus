// src/app/inspector/page.tsx
"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api-client";
import { RequestLog } from "@/types/api";

export default function InspectorPage() {
  const [requests, setRequests] = useState<RequestLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get<RequestLog[]>('/api/admin/inspector/requests?limit=50');
      setRequests(data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading requests...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Request Inspector</h1>
        <Button onClick={fetchRequests}>Refresh</Button>
      </div>

      <div className="space-y-4">
        {requests.map((request) => (
          <Card key={request.id}>
            <CardHeader className="pb-2">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Badge variant={
                      request.request_method === 'GET' ? 'secondary' : 
                      request.request_method === 'POST' ? 'default' : 
                      request.request_method === 'PUT' ? 'outline' : 
                      request.request_method === 'DELETE' ? 'destructive' : 'secondary'
                    }>
                      {request.request_method}
                    </Badge>
                    {request.request_path}
                  </CardTitle>
                  <CardDescription>
                    {new Date(request.created_at).toLocaleString()} • 
                    Status: {request.response_status} • 
                    IP: {request.client_ip}
                  </CardDescription>
                </div>
                <Badge variant={request.response_status >= 200 && request.response_status < 300 ? 'default' : 
                              request.response_status >= 400 && request.response_status < 500 ? 'secondary' : 
                              'destructive'}>
                  {request.response_status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-2">Request</h4>
                  <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
                    {request.request_body ? JSON.stringify(JSON.parse(request.request_body), null, 2) : 'No body'}
                  </pre>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Response</h4>
                  <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
                    {request.response_body ? JSON.stringify(JSON.parse(request.response_body), null, 2) : 'No body'}
                  </pre>
                </div>
              </div>
              <div className="mt-4 flex gap-2">
                <Button variant="outline" size="sm">View Details</Button>
                <Button variant="outline" size="sm">Replay</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}