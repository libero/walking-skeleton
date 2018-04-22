import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { routing } from './app.routing';

import { AppComponent } from './app.component';
import { WorkflowListComponent } from './workflow-list/workflow-list.component';
import { WorkflowDetailComponent } from './workflow-detail/workflow-detail.component';
import { WorkflowService } from "./workflow.service";
import { HttpClientModule } from "@angular/common/http";


@NgModule({
  declarations: [
    AppComponent,
    WorkflowListComponent,
    WorkflowDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    routing,
  ],
  providers: [
    WorkflowService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
