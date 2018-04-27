import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {Observable} from "rxjs/Observable";

@Injectable()
export class WorkflowService {

  apiRoot: string;
  workflowsUrl: string;

  constructor(private http: HttpClient) {
    this.apiRoot = `http://localhost:8000`;
    this.workflowsUrl = `${this.apiRoot}/workflows/api/v1/workflows/`
  }

  getWorkflow(workflowId: string): Observable<any> {
    return this.http.get(`${this.workflowsUrl}${workflowId}/`);
  }

  getWorkflows(): Observable<any> {
    return this.http.get(`${this.workflowsUrl}`);
  }

}
