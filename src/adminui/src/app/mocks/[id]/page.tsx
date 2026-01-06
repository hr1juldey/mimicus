// src/app/mocks/[id]/page.tsx
"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api-client";
import { MockDefinition } from "@/types/api";
import { useParams, useRouter } from "next/navigation";

export default function MockEditorPage() {
  const { id } = useParams();
  const router = useRouter();
  const [mock, setMock] = useState<MockDefinition | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id !== 'new') {
      fetchMock(id as string);
    } else {
      // Initialize with default values for new mock
      setMock({
        id: '',
        name: '',
        enabled: true,
        priority: 1,
        mode: 'mock',
        match: {
          method: 'GET',
          path: '',
        },
        response: {
          status: 200,
          body: '{}',
        },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      });
      setLoading(false);
    }
  }, [id]);

  const fetchMock = async (mockId: string) => {
    try {
      setLoading(true);
      const data = await apiClient.get<MockDefinition>(`/api/admin/mocks/${mockId}`);
      setMock(data);
    } catch (error) {
      console.error('Error fetching mock:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!mock) return;

    try {
      if (id === 'new') {
        await apiClient.post('/api/admin/mocks', mock);
      } else {
        await apiClient.put(`/api/admin/mocks/${mock.id}`, mock);
      }
      router.push('/mocks');
    } catch (error) {
      console.error('Error saving mock:', error);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading mock...</p>
      </div>
    );
  }

  if (!mock) {
    return (
      <div className="container mx-auto py-10">
        <p>Mock not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">
          {id === 'new' ? 'Create New Mock' : `Edit Mock: ${mock.name}`}
        </h1>
        <p className="text-muted-foreground">
          Configure how this mock will respond to incoming requests
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Request Configuration</CardTitle>
              <CardDescription>Define how to match incoming requests</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Method</label>
                <select
                  value={mock.match.method}
                  onChange={(e) => setMock({...mock, match: {...mock.match, method: e.target.value}})}
                  className="w-full p-2 border rounded mt-1"
                >
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                  <option value="PATCH">PATCH</option>
                  <option value="HEAD">HEAD</option>
                  <option value="OPTIONS">OPTIONS</option>
                </select>
              </div>
              
              <div>
                <label className="text-sm font-medium">Path</label>
                <Input
                  value={mock.match.path}
                  onChange={(e) => setMock({...mock, match: {...mock.match, path: e.target.value}})}
                  placeholder="/api/users/:id"
                />
              </div>
              
              <div>
                <label className="text-sm font-medium">Headers (JSON)</label>
                <textarea
                  value={JSON.stringify(mock.match.headers || {}, null, 2)}
                  onChange={(e) => {
                    try {
                      const headers = JSON.parse(e.target.value);
                      setMock({...mock, match: {...mock.match, headers}});
                    } catch (err) {
                      // Handle invalid JSON
                    }
                  }}
                  className="w-full p-2 border rounded mt-1 min-h-[100px]"
                  placeholder='{"Content-Type": "application/json"}'
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Response Configuration</CardTitle>
              <CardDescription>Define how the mock should respond</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Status Code</label>
                <Input
                  type="number"
                  value={mock.response.status}
                  onChange={(e) => setMock({...mock, response: {...mock.response, status: parseInt(e.target.value)}})}
                />
              </div>
              
              <div>
                <label className="text-sm font-medium">Response Body</label>
                <textarea
                  value={mock.response.body}
                  onChange={(e) => setMock({...mock, response: {...mock.response, body: e.target.value}})}
                  className="w-full p-2 border rounded mt-1 min-h-[200px]"
                  placeholder='{"message": "Hello World"}'
                />
              </div>
              
              <div>
                <label className="text-sm font-medium">Headers (JSON)</label>
                <textarea
                  value={JSON.stringify(mock.response.headers || {}, null, 2)}
                  onChange={(e) => {
                    try {
                      const headers = JSON.parse(e.target.value);
                      setMock({...mock, response: {...mock.response, headers}});
                    } catch (err) {
                      // Handle invalid JSON
                    }
                  }}
                  className="w-full p-2 border rounded mt-1 min-h-[100px]"
                  placeholder='{"Content-Type": "application/json"}'
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Mock Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Name</label>
                <Input
                  value={mock.name}
                  onChange={(e) => setMock({...mock, name: e.target.value})}
                  placeholder="My API Mock"
                />
              </div>
              
              <div>
                <label className="text-sm font-medium">Priority</label>
                <Input
                  type="number"
                  value={mock.priority}
                  onChange={(e) => setMock({...mock, priority: parseInt(e.target.value)})}
                />
              </div>
              
              <div className="flex items-center justify-between">
                <span>Enabled</span>
                <Badge variant={mock.enabled ? "default" : "secondary"}>
                  {mock.enabled ? "Active" : "Inactive"}
                </Badge>
              </div>
              
              <div>
                <label className="text-sm font-medium">Mode</label>
                <select
                  value={mock.mode}
                  onChange={(e) => setMock({...mock, mode: e.target.value as 'mock' | 'proxy'})}
                  className="w-full p-2 border rounded mt-1"
                >
                  <option value="mock">Mock</option>
                  <option value="proxy">Proxy</option>
                </select>
              </div>
              
              <Button onClick={handleSave} className="w-full">
                Save Mock
              </Button>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Preview</CardTitle>
              <CardDescription>See how your mock will respond</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted p-4 rounded text-sm overflow-x-auto">
                {JSON.stringify({
                  method: mock.match.method,
                  path: mock.match.path,
                  response: {
                    status: mock.response.status,
                    body: mock.response.body,
                  }
                }, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}