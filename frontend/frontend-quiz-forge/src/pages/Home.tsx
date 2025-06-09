import UploadForm from '../components/UploadForm';

export default function Home() {
  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Upload PDF and Generate Quiz</h2>
      <UploadForm />
    </div>
  );
}
