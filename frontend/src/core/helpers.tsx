import { IBEShallowFlowRun } from "./@types";
import moment from "moment";
import { DATETIME_FORMAT } from "./constants";


export function formatRunStart(run: IBEShallowFlowRun) {
  return run.datetime_created == null ? "Just now" : moment(run.datetime_created, moment.ISO_8601).format(DATETIME_FORMAT)
}

export function formatRunDuration(datetime_created?: string, datetime_end?: string): string {
  if (datetime_created === null && datetime_end !== null) return "Error"
  return datetime_end === null ? "Running" : formatDuration(datetime_created!, datetime_end!)
}

export function formatDuration(datetime_created: string, datetime_end?: string): string {
  return moment.duration(moment(datetime_end!, moment.ISO_8601).diff(moment(datetime_created, moment.ISO_8601))).asMilliseconds() + "ms"
}