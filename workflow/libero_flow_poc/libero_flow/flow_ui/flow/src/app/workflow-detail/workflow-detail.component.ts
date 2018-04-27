import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Subscription} from "rxjs/Subscription";
import {WorkflowService} from "../workflow.service";

@Component({
  selector: 'app-workflow-detail',
  templateUrl: './workflow-detail.component.html',
  styleUrls: ['./workflow-detail.component.sass']
})
export class WorkflowDetailComponent implements OnInit {

  routeSubscription: Subscription;
  workflowId: string;
  workflow = {};

  constructor(private activatedRoute: ActivatedRoute, private workflowService: WorkflowService) { }

  ngOnInit() {

    this.routeSubscription = this.activatedRoute.params.subscribe(
      (params: any) => {
        this.workflowId = params['workflowId'];
        this.getWorkflowData();
      }
    );
  }

  getWorkflowData() {
    this.workflowService.getWorkflow(this.workflowId)
      .subscribe(
        workflow => this.workflow = workflow
    )
  }

}
