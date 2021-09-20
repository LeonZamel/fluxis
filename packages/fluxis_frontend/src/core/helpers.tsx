import { IBEShallowFlowRun } from "./@types";
import moment from "moment";
import { DATETIME_FORMAT } from "./constants";


export function formatRunStart(run: IBEShallowFlowRun) {
  return run.datetime_start === null ? "Just now" : moment(run.datetime_start, moment.ISO_8601).format(DATETIME_FORMAT)
}

export function formatRunDuration(datetime_start?: string, datetime_end?: string): string {
  if (datetime_start === null && datetime_end !== null) return "Error"
  return datetime_end === null ? "Running" : formatDuration(datetime_start!, datetime_end!)
}

export function formatDuration(datetime_start: string, datetime_end?: string): string {
  return moment.duration(moment(datetime_end!, moment.ISO_8601).diff(moment(datetime_start, moment.ISO_8601))).asMilliseconds() + "ms"
}