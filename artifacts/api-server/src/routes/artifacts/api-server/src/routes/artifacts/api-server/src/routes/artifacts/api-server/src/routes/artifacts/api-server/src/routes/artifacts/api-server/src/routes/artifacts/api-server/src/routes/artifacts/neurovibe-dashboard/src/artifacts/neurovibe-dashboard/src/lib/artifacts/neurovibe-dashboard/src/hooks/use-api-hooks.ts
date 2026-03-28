import { useQueryClient } from "@tanstack/react-query";
import {
  useListDevices, useCreateDevice, useUpdateDevice, useDeleteDevice,
  useListSites, useCreateSite, useUpdateSite, useDeleteSite,
  useListUsers, useCreateUser, useUpdateUser, useDeleteUser,
  useListAlerts, useAcknowledgeAlert,
  useGetDevice, useGetDeviceSensorData, useGetDeviceSpectrum, useGetDevicePrediction,
  ListDevicesParams, ListAlertsParams, GetDeviceSensorDataParams
} from "@workspace/api-client-react";

export function useDevices(params?: ListDevicesParams) { return useListDevices(params); }
export function useDevice(id: number) { return useGetDevice(id); }

export function useDeviceMutations() {
  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["/api/devices"] });
  return {
    createDevice: useCreateDevice({ mutation: { onSuccess: invalidate } }),
    updateDevice: useUpdateDevice({ mutation: { onSuccess: invalidate } }),
    deleteDevice: useDeleteDevice({ mutation: { onSuccess: invalidate } }),
  };
}

export function useSites() { return useListSites(); }

export function useSiteMutations() {
  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["/api/sites"] });
  return {
    createSite: useCreateSite({ mutation: { onSuccess: invalidate } }),
    updateSite: useUpdateSite({ mutation: { onSuccess: invalidate } }),
    deleteSite: useDeleteSite({ mutation: { onSuccess: invalidate } }),
  };
}

export function useUsers() { return useListUsers(); }

export function useUserMutations() {
  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["/api/users"] });
  return {
    createUser: useCreateUser({ mutation: { onSuccess: invalidate } }),
    updateUser: useUpdateUser({ mutation: { onSuccess: invalidate } }),
    deleteUser: useDeleteUser({ mutation: { onSuccess: invalidate } }),
  };
}

export function useAlerts(params?: ListAlertsParams) { return useListAlerts(params); }

export function useAlertMutations() {
  const queryClient = useQueryClient();
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["/api/alerts"] });
  return { acknowledgeAlert: useAcknowledgeAlert({ mutation: { onSuccess: invalidate } }) };
}

export function useDeviceData(id: number, sensorParams?: GetDeviceSensorDataParams) {
  const sensorQuery = useGetDeviceSensorData(id, sensorParams);
  const spectrumQuery = useGetDeviceSpectrum(id);
  const predictionQuery = useGetDevicePrediction(id);
  return {
    sensorData: sensorQuery.data, isLoadingSensor: sensorQuery.isLoading,
    spectrumData: spectrumQuery.data, isLoadingSpectrum: spectrumQuery.isLoading,
    predictionData: predictionQuery.data, isLoadingPrediction: predictionQuery.isLoading,
  };
}
